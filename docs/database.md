# 数据库设计文档

## 📊 数据库概述

**数据库：** MySQL 8.0  
**字符集：** utf8mb4  
**引擎：** InnoDB

---

## 📋 数据表设计

### 1. 舆情事件表 (sentiment_events)

存储监控到的舆情事件/文章/视频信息

```sql
CREATE TABLE sentiment_events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    event_id VARCHAR(64) UNIQUE NOT NULL,  -- 平台唯一 ID
    platform VARCHAR(32) NOT NULL,          -- 平台：wechat/douyin/weibo/xiaohongshu/kuaishou/jinritoutiao
    event_type VARCHAR(32) NOT NULL,        -- 类型：article/video/post/comment
    title VARCHAR(500),                     -- 标题
    content TEXT,                           -- 内容
    author VARCHAR(200),                    -- 作者/发布者
    author_id VARCHAR(100),                 -- 作者 ID
    publish_time DATETIME,                  -- 发布时间
    url VARCHAR(1000),                      -- 原文链接
    cover_image VARCHAR(500),               -- 封面图
    
    -- 互动数据
    view_count INT DEFAULT 0,               -- 阅读量/播放量
    like_count INT DEFAULT 0,               -- 点赞数
    comment_count INT DEFAULT 0,            -- 评论数
    share_count INT DEFAULT 0,              -- 分享数
    
    -- 情感分析
    sentiment_score DECIMAL(3,2),           -- 情感得分：-1.00 ~ 1.00
    sentiment_label VARCHAR(16),            -- 情感标签：positive/negative/neutral
    confidence DECIMAL(3,2),                -- 置信度
    
    -- 关键词匹配
    matched_keywords JSON,                  -- 匹配的关键词列表
    keyword_score INT DEFAULT 0,            -- 关键词匹配度
    
    -- 热度计算
    heat_score INT DEFAULT 0,               -- 热度值
    is_trending BOOLEAN DEFAULT FALSE,      -- 是否热门
    
    -- 告警状态
    alert_status VARCHAR(16) DEFAULT 'none', -- none/pending/sent/ignored
    alert_level VARCHAR(16) DEFAULT 'low',   -- low/medium/high/critical
    alert_time DATETIME,                    -- 告警时间
    
    -- 元数据
    raw_data JSON,                          -- 原始数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_platform (platform),
    INDEX idx_publish_time (publish_time),
    INDEX idx_sentiment (sentiment_label),
    INDEX idx_heat_score (heat_score),
    INDEX idx_alert_status (alert_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='舆情事件表';
```

---

### 2. 关键词配置表 (keywords)

监控的关键词配置

```sql
CREATE TABLE keywords (
    id INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(100) UNIQUE NOT NULL,   -- 关键词
    category VARCHAR(32),                   -- 分类：brand/product/competitor/industry
    weight INT DEFAULT 1,                   -- 权重
    is_active BOOLEAN DEFAULT TRUE,         -- 是否启用
    negative BOOLEAN DEFAULT FALSE,         -- 是否负面关键词
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关键词配置表';
```

---

### 3. 评论表 (comments)

舆情事件的评论数据

```sql
CREATE TABLE comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    comment_id VARCHAR(64) UNIQUE NOT NULL, -- 平台评论 ID
    event_id BIGINT NOT NULL,               -- 关联舆情事件 ID
    platform VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,                  -- 评论内容
    author VARCHAR(200),                    -- 评论者
    author_id VARCHAR(100),                 -- 评论者 ID
    publish_time DATETIME,                  -- 评论时间
    
    -- 互动数据
    like_count INT DEFAULT 0,
    reply_count INT DEFAULT 0,
    
    -- 情感分析
    sentiment_score DECIMAL(3,2),
    sentiment_label VARCHAR(16),
    
    -- 父评论（回复链）
    parent_comment_id VARCHAR(64),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_event_id (event_id),
    INDEX idx_platform (platform),
    INDEX idx_publish_time (publish_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';
```

---

### 4. 告警记录表 (alerts)

告警通知记录

```sql
CREATE TABLE alerts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    alert_id VARCHAR(64) UNIQUE NOT NULL,
    event_id BIGINT NOT NULL,               -- 关联舆情事件
    level VARCHAR(16) NOT NULL,             -- low/medium/high/critical
    title VARCHAR(200) NOT NULL,
    content TEXT,
    channel VARCHAR(32),                    -- wechat/dingding/email
    status VARCHAR(16) DEFAULT 'pending',   -- pending/sent/failed
    sent_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_event_id (event_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='告警记录表';
```

---

### 5. 数据统计表 (statistics_daily)

每日统计数据

```sql
CREATE TABLE statistics_daily (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stat_date DATE UNIQUE NOT NULL,
    
    -- 事件统计
    total_events INT DEFAULT 0,
    positive_events INT DEFAULT 0,
    negative_events INT DEFAULT 0,
    neutral_events INT DEFAULT 0,
    
    -- 平台统计
    wechat_events INT DEFAULT 0,
    douyin_events INT DEFAULT 0,
    weibo_events INT DEFAULT 0,
    
    -- 告警统计
    total_alerts INT DEFAULT 0,
    critical_alerts INT DEFAULT 0,
    
    -- 互动统计
    total_views INT DEFAULT 0,
    total_likes INT DEFAULT 0,
    total_comments INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_stat_date (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日统计表';
```

---

### 6. API 配置表 (api_configs)

第三方 API 配置

```sql
CREATE TABLE api_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    provider VARCHAR(64) NOT NULL,          -- 服务商：xinbang/weihot/qingbo
    api_name VARCHAR(100) NOT NULL,         -- API 名称
    api_key VARCHAR(200),                   -- API 密钥
    api_secret VARCHAR(200),                -- API 密钥
    endpoint VARCHAR(500),                  -- API 端点
    rate_limit INT DEFAULT 100,             -- 每分钟调用限制
    daily_quota INT DEFAULT 1000,           -- 每日配额
    used_today INT DEFAULT 0,               -- 今日已用
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API 配置表';
```

---

## 🔗 表关系

```
sentiment_events (1) ──→ (N) comments
sentiment_events (1) ──→ (1) alerts
keywords ──→ (N) sentiment_events (通过 matched_keywords)
```

---

## 📊 初始化数据

```sql
-- 初始化关键词
INSERT INTO keywords (keyword, category, weight, negative) VALUES
('WaveUP', 'brand', 10, FALSE),
('WaveUP 科技', 'brand', 8, FALSE),
('WaveUP 产品', 'product', 5, FALSE),
-- 添加竞品关键词
('竞品 A', 'competitor', 3, FALSE),
('竞品 B', 'competitor', 3, FALSE),
-- 添加负面关键词
('WaveUP 投诉', 'brand', 10, TRUE),
('WaveUP 质量问题', 'product', 10, TRUE);

-- 初始化 API 配置（根据实际购买的服务填写）
INSERT INTO api_configs (provider, api_name, api_key, endpoint, rate_limit) VALUES
('xinbang', 'article_search', 'YOUR_API_KEY', 'https://api.newrank.cn/...', 100),
('xinbang', 'video_search', 'YOUR_API_KEY', 'https://api.newrank.cn/...', 100);
```

---

**设计时间：** 2026-03-08  
**设计负责人：** OpenClaw
