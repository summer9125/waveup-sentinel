"""
数据模型定义
"""
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Boolean, DECIMAL, JSON, TIMESTAMP, Index, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class SentimentEvent(Base):
    """舆情事件表"""
    __tablename__ = 'sentiment_events'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(String(64), unique=True, nullable=False, comment='平台唯一 ID')
    platform = Column(String(32), nullable=False, comment='平台：wechat/douyin/weibo/xiaohongshu/kuaishou/jinritoutiao')
    event_type = Column(String(32), nullable=False, comment='类型：article/video/post/comment')
    title = Column(String(500), comment='标题')
    content = Column(Text, comment='内容')
    author = Column(String(200), comment='作者/发布者')
    author_id = Column(String(100), comment='作者 ID')
    publish_time = Column(DateTime, comment='发布时间')
    url = Column(String(1000), comment='原文链接')
    cover_image = Column(String(500), comment='封面图')
    
    # 互动数据
    view_count = Column(Integer, default=0, comment='阅读量/播放量')
    like_count = Column(Integer, default=0, comment='点赞数')
    comment_count = Column(Integer, default=0, comment='评论数')
    share_count = Column(Integer, default=0, comment='分享数')
    
    # 情感分析
    sentiment_score = Column(DECIMAL(3, 2), comment='情感得分：-1.00 ~ 1.00')
    sentiment_label = Column(String(16), comment='情感标签：positive/negative/neutral')
    confidence = Column(DECIMAL(3, 2), comment='置信度')
    
    # 关键词匹配
    matched_keywords = Column(JSON, comment='匹配的关键词列表')
    keyword_score = Column(Integer, default=0, comment='关键词匹配度')
    
    # 热度计算
    heat_score = Column(Integer, default=0, comment='热度值')
    is_trending = Column(Boolean, default=False, comment='是否热门')
    
    # 告警状态
    alert_status = Column(String(16), default='none', comment='none/pending/sent/ignored')
    alert_level = Column(String(16), default='low', comment='low/medium/high/critical')
    alert_time = Column(DateTime, comment='告警时间')
    
    # 元数据
    raw_data = Column(JSON, comment='原始数据')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_platform', 'platform'),
        Index('idx_publish_time', 'publish_time'),
        Index('idx_sentiment', 'sentiment_label'),
        Index('idx_heat_score', 'heat_score'),
        Index('idx_alert_status', 'alert_status'),
    )


class Keyword(Base):
    """关键词配置表"""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(100), unique=True, nullable=False, comment='关键词')
    category = Column(String(32), comment='分类：brand/product/competitor/industry')
    weight = Column(Integer, default=1, comment='权重')
    is_active = Column(Boolean, default=True, comment='是否启用')
    negative = Column(Boolean, default=False, comment='是否负面关键词')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        Index('idx_category', 'category'),
        Index('idx_active', 'is_active'),
    )


class Comment(Base):
    """评论表"""
    __tablename__ = 'comments'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    comment_id = Column(String(64), unique=True, nullable=False, comment='平台评论 ID')
    event_id = Column(BigInteger, ForeignKey('sentiment_events.id'), nullable=False, comment='关联舆情事件 ID')
    platform = Column(String(32), nullable=False)
    content = Column(Text, nullable=False, comment='评论内容')
    author = Column(String(200), comment='评论者')
    author_id = Column(String(100), comment='评论者 ID')
    publish_time = Column(DateTime, comment='评论时间')
    
    # 互动数据
    like_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    
    # 情感分析
    sentiment_score = Column(DECIMAL(3, 2))
    sentiment_label = Column(String(16))
    
    # 父评论（回复链）
    parent_comment_id = Column(String(64))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        Index('idx_event_id', 'event_id'),
        Index('idx_platform', 'platform'),
        Index('idx_publish_time', 'publish_time'),
    )


class Alert(Base):
    """告警记录表"""
    __tablename__ = 'alerts'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    alert_id = Column(String(64), unique=True, nullable=False)
    event_id = Column(BigInteger, ForeignKey('sentiment_events.id'), nullable=False, comment='关联舆情事件')
    level = Column(String(16), nullable=False, comment='low/medium/high/critical')
    title = Column(String(200), nullable=False)
    content = Column(Text)
    channel = Column(String(32), comment='wechat/dingding/email')
    status = Column(String(16), default='pending', comment='pending/sent/failed')
    sent_at = Column(DateTime)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        Index('idx_event_id', 'event_id'),
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
    )


class StatisticsDaily(Base):
    """每日统计表"""
    __tablename__ = 'statistics_daily'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stat_date = Column(DateTime, unique=True, nullable=False)
    
    # 事件统计
    total_events = Column(Integer, default=0)
    positive_events = Column(Integer, default=0)
    negative_events = Column(Integer, default=0)
    neutral_events = Column(Integer, default=0)
    
    # 平台统计
    wechat_events = Column(Integer, default=0)
    douyin_events = Column(Integer, default=0)
    weibo_events = Column(Integer, default=0)
    
    # 告警统计
    total_alerts = Column(Integer, default=0)
    critical_alerts = Column(Integer, default=0)
    
    # 互动统计
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_stat_date', 'stat_date'),
    )
