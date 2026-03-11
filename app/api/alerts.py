"""
预警系统 API
"""
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import List
import random

router = APIRouter()

# 模拟预警数据
ALERTS = [
    {
        "id": 1,
        "level": "high",
        "title": "微博出现负面话题讨论",
        "content": "WaveUP 相关负面话题在微博平台快速传播，2 小时内讨论量增长 300%",
        "source": "微博",
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "status": "active",
        "metric": "sentiment_drop",
        "impact_score": 85
    },
    {
        "id": 2,
        "level": "medium",
        "title": "竞品发布新产品",
        "content": "竞品 A 发布新款数字藏品平台，社交媒体讨论热度上升",
        "source": "知乎",
        "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        "status": "active",
        "metric": "competitor_activity",
        "impact_score": 65
    },
    {
        "id": 3,
        "level": "low",
        "title": "用户投诉增加",
        "content": "客服相关投诉在 24 小时内增加 15 条",
        "source": "黑猫投诉",
        "timestamp": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        "status": "resolved",
        "metric": "complaints",
        "impact_score": 45
    }
]

@router.get("/list", summary="获取预警列表")
async def get_alerts(
    level: str = Query("all", description="all|high|medium|low"),
    status: str = Query("all", description="all|active|resolved"),
    limit: int = Query(20, ge=1, le=100)
):
    """获取预警列表"""
    alerts = ALERTS.copy()
    
    if level != "all":
        alerts = [a for a in alerts if a["level"] == level]
    if status != "all":
        alerts = [a for a in alerts if a["status"] == status]
    
    return {
        "code": 0,
        "data": alerts[:limit],
        "total": len(alerts)
    }

@router.get("/stats", summary="获取预警统计")
async def get_alert_stats():
    """获取预警统计数据"""
    return {
        "code": 0,
        "data": {
            "total": len(ALERTS),
            "active": sum(1 for a in ALERTS if a["status"] == "active"),
            "high": sum(1 for a in ALERTS if a["level"] == "high"),
            "medium": sum(1 for a in ALERTS if a["level"] == "medium"),
            "low": sum(1 for a in ALERTS if a["level"] == "low"),
            "trend": "down"  # 预警数量趋势
        }
    }

@router.post("/acknowledge", summary="确认预警")
async def acknowledge_alert(alert_id: int):
    """确认并处理预警"""
    for alert in ALERTS:
        if alert["id"] == alert_id:
            alert["status"] = "resolved"
            return {"code": 0, "message": "预警已确认"}
    return {"code": 404, "message": "预警不存在"}
