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

# 标签体系
TAGS = {
    "categories": ["行业资讯", "公司动态", "产品发布", "用户反馈", "竞品分析", "政策法规", "市场趋势", "技术创新"],
    "channels": ["微博", "知乎", "小红书", "抖音", "B 站", "微信公众号", "今日头条", "Twitter", "Discord", "Telegram"],
    "content_types": ["资讯", "评论", "问答", "视频", "直播", "图文", "报告"],
    "industries": ["数字藏品", "NFT", "元宇宙", "区块链", "文化 IP", "Web3.0", "人工智能", "虚拟现实"]
}

# 模拟实时动态
def generate_realtime_feed():
    feed = []
    for i in range(50):
        # 随机生成标签
        category = random.choice(TAGS["categories"])
        channel = random.choice(TAGS["channels"])
        content_type = random.choice(TAGS["content_types"])
        industry = random.choice(TAGS["industries"])
        tags = [category, industry, content_type]
        
        # 情感分析
        sentiment = random.choices(["positive", "neutral", "negative"], weights=[0.6, 0.3, 0.1])[0]
        sentiment_score = round(random.uniform(0.7, 1.0) if sentiment == "positive" else random.uniform(0, 0.4) if sentiment == "negative" else random.uniform(0.4, 0.6), 2)
        
        # 内容生成
        contents = {
            "行业资讯": f"{industry}领域最新动态：市场交易额环比增长{random.randint(10, 50)}%",
            "公司动态": f"WaveUP {random.choice(['发布', '更新', '推出', '上线'])}新功能，用户反响热烈",
            "产品发布": f"新一代{industry}平台上线，首日用户突破{random.randint(1, 10)}万",
            "用户反馈": f"用户对{random.choice(['产品体验', '功能设计', '服务质量'])}表示{random.choice(['满意', '期待', '关注'])}",
            "竞品分析": f"竞品平台{random.choice(['融资', '发布', '合作']}消息，行业竞争加剧",
            "政策法规": f"{random.choice(['相关部门', '行业协会'])}发布{industry}领域新规",
            "市场趋势": f"{industry}市场持续增长，预计{random.randint(2026, 2030)}年规模达{random.randint(100, 1000)}亿",
            "技术创新": f"{random.choice(['AI', '区块链', 'VR/AR'])}技术在{industry}领域应用取得突破"
        }
        
        feed.append({
            "id": i + 1,
            "content": contents.get(category, f"{category}相关内容"),
            "summary": f"这是关于{category}的详细内容分析，涉及{industry}领域。该事件在{channel}平台引发讨论，用户反馈积极。",
            "source": channel,
            "source_url": f"https://{channel.lower().replace('站', '')}.com",
            "content_type": content_type,
            "category": category,
            "industry": industry,
            "tags": tags,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "author": f"{random.choice(['官方账号', '行业媒体', '知名博主', '普通用户', '认证机构'])}_{random.randint(1000, 9999)}",
            "author_avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={i}",
            "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(1, 720))).isoformat(),
            "engagement": {
                "likes": random.randint(0, 10000),
                "comments": random.randint(0, 2000),
                "shares": random.randint(0, 1000),
                "views": random.randint(100, 100000)
            },
            "is_verified": random.random() > 0.7,
            "is_important": random.random() > 0.8,
            "heat_score": round(random.uniform(50, 100), 1)
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

@router.get("/tags", summary="获取标签体系")
async def get_tags():
    """获取完整的标签体系"""
    return {
        "code": 0,
        "data": TAGS
    }

@router.get("/recommend", summary="个性化推荐")
async def get_recommendations(
    user_tags: str = Query("", description="用户偏好标签，逗号分隔"),
    limit: int = Query(10, ge=1, le=50)
):
    """基于用户偏好的个性化推荐（类似今日头条）"""
    feed = generate_realtime_feed()
    
    # 如果用户有偏好标签，进行加权推荐
    if user_tags:
        pref_tags = [t.strip() for t in user_tags.split(",")]
        for item in feed:
            # 标签匹配加分
            for tag in item.get("tags", []):
                if tag in pref_tags:
                    item["heat_score"] = item.get("heat_score", 50) * 1.5
            # 分类匹配加分
            if item.get("category") in pref_tags:
                item["heat_score"] = item.get("heat_score", 50) * 1.3
            # 行业匹配加分
            if item.get("industry") in pref_tags:
                item["heat_score"] = item.get("heat_score", 50) * 1.2
    
    # 按热度排序
    feed.sort(key=lambda x: x.get("heat_score", 0), reverse=True)
    
    return {
        "code": 0,
        "data": feed[:limit]
    }

@router.post("/like", summary="点赞")
async def like_item(item_id: int = Body(..., embed=True)):
    """点赞操作"""
    return {
        "code": 0,
        "message": "点赞成功",
        "data": {"item_id": item_id, "liked": True}
    }

@router.post("/collect", summary="收藏")
async def collect_item(item_id: int = Body(..., embed=True)):
    """收藏操作"""
    return {
        "code": 0,
        "message": "收藏成功",
        "data": {"item_id": item_id, "collected": True}
    }
