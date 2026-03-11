"""
实时监控 API
"""
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import List, Optional
import random

router = APIRouter()

# 模拟监控数据
MONITORING_DATA = {
    "waveup": {
        "total_mentions": 1247,
        "sentiment_score": 0.72,
        "trend": "up",
        "change_24h": 15.3
    },
    "competitors": [
        {"name": "竞品 A", "mentions": 856, "sentiment": 0.65},
        {"name": "竞品 B", "mentions": 623, "sentiment": 0.58},
        {"name": "竞品 C", "mentions": 445, "sentiment": 0.71}
    ]
}

# 模拟实时动态
def generate_realtime_feed():
    sources = ["微博", "知乎", "小红书", "抖音", "Twitter", "Discord"]
    sentiments = ["positive", "neutral", "negative"]
    topics = ["数字藏品", "NFT", "文化 IP", "元宇宙", "区块链", "WaveUP 平台"]
    
    feed = []
    for i in range(20):
        sentiment = random.choices(sentiments, weights=[0.6, 0.3, 0.1])[0]
        feed.append({
            "id": i + 1,
            "content": f"{random.choice(topics)}相关讨论：这是模拟的舆情内容 #{i+1}",
            "source": random.choice(sources),
            "sentiment": sentiment,
            "sentiment_score": random.uniform(0.5, 1.0) if sentiment == "positive" else random.uniform(0, 0.5),
            "author": f"user_{random.randint(1000, 9999)}",
            "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(1, 120))).isoformat(),
            "likes": random.randint(0, 500),
            "comments": random.randint(0, 100),
            "shares": random.randint(0, 50)
        })
    return feed

@router.get("/overview", summary="获取监控概览")
async def get_overview():
    """获取舆情监控概览数据"""
    return {
        "code": 0,
        "data": {
            "waveup": MONITORING_DATA["waveup"],
            "competitors": MONITORING_DATA["competitors"],
            "last_update": datetime.utcnow().isoformat()
        }
    }

@router.get("/feed", summary="获取实时动态")
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    sentiment: Optional[str] = None,
    source: Optional[str] = None
):
    """获取实时舆情动态"""
    feed = generate_realtime_feed()[:limit]
    
    if sentiment:
        feed = [f for f in feed if f["sentiment"] == sentiment]
    if source:
        feed = [f for f in feed if f["source"] == source]
    
    return {
        "code": 0,
        "data": feed,
        "total": len(feed)
    }

@router.get("/trend", summary="获取趋势数据")
async def get_trend(
    days: int = Query(7, ge=1, le=30),
    metric: str = Query("mentions", description="mentions|sentiment")
):
    """获取趋势数据"""
    base = 1000 if metric == "mentions" else 0.7
    trend_data = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        value = base + random.uniform(-200, 200) if metric == "mentions" else base + random.uniform(-0.1, 0.1)
        trend_data.append({
            "date": date,
            "value": round(value, 2),
            "waveup": round(value * 1.1, 2),
            "competitor_avg": round(value * 0.8, 2)
        })
    
    return {
        "code": 0,
        "data": trend_data
    }

@router.get("/topics", summary="获取热门话题")
async def get_topics(limit: int = Query(10, ge=1, le=20)):
    """获取热门话题"""
    topics = [
        {"keyword": "WaveUP 数字藏品", "count": 456, "sentiment": 0.75, "trend": "up"},
        {"keyword": "NFT 市场", "count": 389, "sentiment": 0.68, "trend": "stable"},
        {"keyword": "文化 IP 授权", "count": 267, "sentiment": 0.72, "trend": "up"},
        {"keyword": "元宇宙平台", "count": 234, "sentiment": 0.65, "trend": "down"},
        {"keyword": "区块链艺术", "count": 198, "sentiment": 0.70, "trend": "stable"},
        {"keyword": "数字版权", "count": 176, "sentiment": 0.62, "trend": "up"},
        {"keyword": "虚拟展览", "count": 145, "sentiment": 0.68, "trend": "stable"},
        {"keyword": "Web3.0", "count": 132, "sentiment": 0.71, "trend": "up"},
        {"keyword": "数字收藏", "count": 118, "sentiment": 0.66, "trend": "stable"},
        {"keyword": "IP 运营", "count": 95, "sentiment": 0.69, "trend": "up"}
    ]
    return {
        "code": 0,
        "data": topics[:limit]
    }
