# WaveUP Sentinel Frontend

舆情监控系统前端 - Vue3 + Vite + Element Plus

## 🚀 快速启动

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build
```

## 📁 目录结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   │   └── index.js
│   ├── assets/           # 静态资源
│   ├── components/       # 组件
│   │   ├── Dashboard.vue     # 仪表盘
│   │   ├── EventList.vue     # 事件列表
│   │   ├── SentimentChart.vue # 情感分析图表
│   │   └── AlertPanel.vue    # 告警面板
│   ├── views/            # 页面
│   │   ├── Home.vue
│   │   ├── Events.vue
│   │   ├── Analysis.vue
│   │   └── Settings.vue
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 技术栈

- **框架：** Vue 3
- **构建工具：** Vite
- **UI 组件库：** Element Plus
- **图表库：** ECharts
- **HTTP 客户端：** Axios

## 📊 功能模块

1. **仪表盘** - 舆情概览、实时数据
2. **事件管理** - 事件列表、详情、搜索
3. **情感分析** - 情感趋势、分布图表
4. **告警中心** - 告警列表、处理状态
5. **系统设置** - 关键词配置、API 配置

---

**创建时间：** 2026-03-08  
**开发者：** 开阳 ⭐
