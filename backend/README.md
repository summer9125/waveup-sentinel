# WaveUP Sentinel Backend

舆情监控系统后端服务 - Python FastAPI

## 🚀 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填写数据库和 API 配置

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── event.py         # 舆情事件模型
│   │   ├── keyword.py       # 关键词模型
│   │   ├── comment.py       # 评论模型
│   │   └── alert.py         # 告警模型
│   ├── schemas/             # Pydantic 模式
│   │   ├── __init__.py
│   │   └── event.py
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── events.py        # 事件管理
│   │   ├── keywords.py      # 关键词管理
│   │   ├── alerts.py        # 告警管理
│   │   └── stats.py         # 统计数据
│   ├── services/            # 业务服务
│   │   ├── __init__.py
│   │   ├── collector.py     # 数据采集
│   │   ├── analyzer.py      # 情感分析
│   │   ├── alerter.py       # 告警通知
│   │   └── reporter.py      # 报告生成
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── sentiment.py     # 情感分析工具
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 技术栈

- **框架：** FastAPI
- **数据库：** MySQL 8.0 + SQLAlchemy
- **缓存：** Redis
- **任务队列：** Celery（可选）
- **情感分析：** SnowNLP / 百度 AI

## 📝 API 文档

启动后访问：http://localhost:8000/docs

---

**创建时间：** 2026-03-08
