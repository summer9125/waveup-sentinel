"""
API 路由 - 事件管理
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SentimentEvent, Keyword
from datetime import datetime

router = APIRouter()


@router.get("/")
async def list_events(
    skip: int = 0,
    limit: int = 50,
    platform: str = None,
    sentiment: str = None,
    db: Session = Depends(get_db)
):
    """获取舆情事件列表"""
    query = db.query(SentimentEvent)
    
    if platform:
        query = query.filter(SentimentEvent.platform == platform)
    if sentiment:
        query = query.filter(SentimentEvent.sentiment_label == sentiment)
    
    events = query.order_by(SentimentEvent.publish_time.desc()).offset(skip).limit(limit).all()
    return {"total": query.count(), "events": events}


@router.get("/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取单个事件详情"""
    event = db.query(SentimentEvent).filter(SentimentEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return event


@router.post("/keywords")
async def add_keyword(
    keyword: str,
    category: str = "brand",
    weight: int = 1,
    negative: bool = False,
    db: Session = Depends(get_db)
):
    """添加监控关键词"""
    existing = db.query(Keyword).filter(Keyword.keyword == keyword).first()
    if existing:
        raise HTTPException(status_code=400, detail="关键词已存在")
    
    new_keyword = Keyword(
        keyword=keyword,
        category=category,
        weight=weight,
        negative=negative
    )
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)
    return new_keyword


@router.get("/keywords")
async def list_keywords(db: Session = Depends(get_db)):
    """获取所有监控关键词"""
    keywords = db.query(Keyword).filter(Keyword.is_active == True).all()
    return {"keywords": keywords}
