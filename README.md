# WaveUP Sentinel 舆情监督系统

> 数字文化资产行情舆情监控平台

## 🎯 功能

- **实时监控** - 全网舆情数据采集
- **情感分析** - AI 驱动的情感倾向识别
- **预警系统** - 负面舆情即时告警
- **趋势分析** - 声量变化趋势追踪
- **竞品对比** - 竞争对手动态监测
- **报告生成** - 自动化舆情报告

## 🛠️ 技术栈

- **后端**: FastAPI + Python
- **前端**: Material Design 3
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **NLP**: jieba + snowNLP (中文情感分析)
- **部署**: Vercel / Railway

## 📊 数据源

### 国内平台
- 微博
- 微信公众号
- 知乎
- 小红书
- 抖音
- 百度贴吧

### 海外平台
- Twitter/X
- Discord
- Telegram
- Reddit

## 🚀 快速开始

```bash
cd waveup-sentinel
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

访问：http://localhost:8000

---

**WaveUP 航海计划** | 数据智能中心
