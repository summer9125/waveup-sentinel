"""
WaveUP Sentinel - 舆情监控系统
FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import events, keywords, alerts, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理资源
    pass


app = FastAPI(
    title="WaveUP Sentinel",
    description="舆情监控系统 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


# 注册路由
app.include_router(events.router, prefix="/api/v1/events", tags=["事件管理"])
app.include_router(keywords.router, prefix="/api/v1/keywords", tags=["关键词管理"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["告警管理"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["统计数据"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
