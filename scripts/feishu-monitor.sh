# 飞书消息自动回复监控脚本

# 每 5 分钟检查一次飞书消息日志
# 检测到新消息后触发 OpenClaw 事件通知

#!/bin/bash

LOG_FILE="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
STATE_FILE="/tmp/feishu-monitor-state.json"

# 获取上次检查的位置
if [ -f "$STATE_FILE" ]; then
    LAST_LINE=$(cat "$STATE_FILE")
else
    LAST_LINE=0
fi

# 检查新消息
NEW_MESSAGES=$(tail -n +$((LAST_LINE + 1)) "$LOG_FILE" 2>/dev/null | grep "feishu.*received message" | tail -1)

if [ -n "$NEW_MESSAGES" ]; then
    # 提取发送者
    SENDER=$(echo "$NEW_MESSAGES" | grep -o "ou_[a-z0-9]*" | head -1)
    
    # 触发 OpenClaw 事件
    openclaw system event --text "📱 飞书新消息 from $SENDER" --mode now
    
    echo "检测到飞书消息 from $SENDER"
fi

# 更新状态
wc -l < "$LOG_FILE" > "$STATE_FILE"
