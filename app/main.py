"""
WaveUP Sentinel - 舆情监督系统
FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api import sentiment, monitoring, alerts, reports

app = FastAPI(
    title="WaveUP Sentinel",
    description="数字文化资产行情舆情监督系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "WaveUP Sentinel", "version": "1.0.0"}

# 首页
@app.get("/")
async def index():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return FileResponse(os.path.join(static_path, "index.html"))

# API 路由
app.include_router(sentiment.router, prefix="/api/v1/sentiment", tags=["情感分析"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["实时监控"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["预警系统"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["报告生成"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
