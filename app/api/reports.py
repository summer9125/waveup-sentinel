"""
报告生成 API
"""
from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/daily", summary="获取日报")
async def get_daily_report():
    """获取每日舆情报告"""
    return {
        "code": 0,
        "data": {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "summary": {
                "total_mentions": 1247,
                "sentiment_score": 0.72,
                "positive_rate": 0.65,
                "negative_rate": 0.12,
                "alerts_count": 3
            },
            "top_topics": [
                {"keyword": "WaveUP 数字藏品", "count": 456},
                {"keyword": "NFT 市场", "count": 389},
                {"keyword": "文化 IP", "count": 267}
            ],
            "top_sources": [
                {"source": "微博", "count": 423},
                {"source": "知乎", "count": 312},
                {"source": "小红书", "count": 256}
            ]
        }
    }

@router.get("/weekly", summary="获取周报")
async def get_weekly_report():
    """获取每周舆情报告"""
    return {
        "code": 0,
        "data": {
            "week": datetime.utcnow().strftime("%Y-W%W"),
            "summary": {
                "total_mentions": 8734,
                "sentiment_score": 0.70,
                "positive_rate": 0.63,
                "negative_rate": 0.14,
                "alerts_count": 12
            },
            "trend": "stable",
            "insights": [
                "WaveUP 品牌声量环比增长 15%",
                "情感倾向保持正面，得分 0.70",
                "主要讨论集中在数字藏品和文化 IP 领域"
            ]
        }
    }
