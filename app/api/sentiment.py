"""
情感分析 API
"""
from fastapi import APIRouter, Body
from datetime import datetime
from typing import List
from snownlp import SnowNLP

router = APIRouter()

@router.post("/analyze", summary="分析文本情感")
async def analyze_sentiment(text: str = Body(..., embed=True)):
    """分析单条文本的情感倾向"""
    s = SnowNLP(text)
    sentiment_score = s.sentiments  # 0-1, 越接近 1 越正面
    
    if sentiment_score > 0.6:
        sentiment = "positive"
        label = "正面"
    elif sentiment_score > 0.4:
        sentiment = "neutral"
        label = "中性"
    else:
        sentiment = "negative"
        label = "负面"
    
    return {
        "code": 0,
        "data": {
            "text": text,
            "sentiment": sentiment,
            "label": label,
            "score": round(sentiment_score, 3),
            "keywords": s.keywords(3),
            "summary": s.summary(1)[0] if s.summary(1) else ""
        }
    }

@router.post("/batch", summary="批量分析")
async def batch_analyze(texts: List[str] = Body(...)):
    """批量分析文本情感"""
    results = []
    for text in texts[:50]:  # 限制 50 条
        s = SnowNLP(text)
        score = s.sentiments
        sentiment = "positive" if score > 0.6 else "neutral" if score > 0.4 else "negative"
        results.append({
            "text": text[:100],
            "sentiment": sentiment,
            "score": round(score, 3)
        })
    
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    positive_count = sum(1 for r in results if r["sentiment"] == "positive")
    negative_count = sum(1 for r in results if r["sentiment"] == "negative")
    
    return {
        "code": 0,
        "data": {
            "results": results,
            "statistics": {
                "total": len(results),
                "positive": positive_count,
                "neutral": len(results) - positive_count - negative_count,
                "negative": negative_count,
                "avg_score": round(avg_score, 3)
            }
        }
    }
