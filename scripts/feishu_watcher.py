#!/usr/bin/env python3
"""
飞书消息实时监控 - 自动检测并通知

功能：
1. 监控飞书消息日志
2. 检测新消息到达
3. 触发 OpenClaw 事件通知
4. 记录已处理消息避免重复

运行方式：
- 手动：python3 feishu_watcher.py
- 定时：*/1 * * * * python3 /path/to/feishu_watcher.py
- 后台：nohup python3 feishu_watcher.py &
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
LOG_FILE = Path("/tmp/openclaw/openclaw-{}.log".format(datetime.now().strftime("%Y-%m-%d")))
STATE_FILE = Path("/tmp/feishu_watcher_state.json")
CHECK_INTERVAL = 10  # 秒

class FeishuWatcher:
    def __init__(self):
        self.state = self.load_state()
        self.last_check_time = datetime.now()
    
    def load_state(self):
        """加载状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_line": 0,
            "processed_messages": [],
            "last_message_time": None
        }
    
    def save_state(self):
        """保存状态"""
        # 只保留最近 100 条消息记录
        self.state["processed_messages"] = self.state["processed_messages"][-100:]
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_log_file(self):
        """获取今天的日志文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = Path(f"/tmp/openclaw/openclaw-{today}.log")
        if log_file.exists():
            return log_file
        # 如果今天的日志不存在，找最新的
        log_dir = Path("/tmp/openclaw/")
        logs = sorted(log_dir.glob("openclaw-*.log"), reverse=True)
        return logs[0] if logs else None
    
    def check_new_messages(self):
        """检查新消息"""
        log_file = self.get_log_file()
        if not log_file or not log_file.exists():
            return []
        
        new_messages = []
        
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            # 从上次检查的位置开始
            start_line = self.state.get("last_line", 0)
            
            for i, line in enumerate(lines[start_line:], start=start_line):
                if "feishu[default]: received message" in line:
                    # 提取消息信息
                    message_info = self.parse_message_line(line)
                    if message_info:
                        msg_id = f"{message_info['sender']}_{message_info['time']}"
                        if msg_id not in self.state["processed_messages"]:
                            new_messages.append(message_info)
                            self.state["processed_messages"].append(msg_id)
            
            # 更新最后检查位置
            self.state["last_line"] = len(lines)
            self.save_state()
            
        except Exception as e:
            print(f"Error checking messages: {e}", file=sys.stderr)
        
        return new_messages
    
    def parse_message_line(self, line):
        """解析日志行"""
        try:
            # 提取时间
            time_part = line.split('"time":"')[1].split('"')[0] if '"time":"' in line else None
            
            # 提取发送者
            sender_part = line.split('from ')[1].split(' in ')[0] if 'from ' in line else None
            
            # 提取聊天类型
            chat_type = "p2p" if "(p2p)" in line else "group"
            
            if sender_part and time_part:
                return {
                    "sender": sender_part,
                    "time": time_part,
                    "chat_type": chat_type,
                    "detected_at": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error parsing line: {e}", file=sys.stderr)
        
        return None
    
    def notify(self, message_info):
        """检测新消息，但不自动回复 - 避免打扰用户"""
        sender = message_info["sender"]
        time = message_info["time"]
        
        # 只记录，不自动回复
        print(f"📱 检测到飞书消息：{sender} at {time}")
        print(f"   (不自动回复 - 等待用户明确指令)")
    
    def run_once(self):
        """运行一次检查"""
        new_messages = self.check_new_messages()
        
        for msg in new_messages:
            self.notify(msg)
            self.state["last_message_time"] = msg["time"]
        
        self.save_state()
        return len(new_messages)
    
    def run_daemon(self):
        """守护进程模式"""
        print(f"🚀 飞书监控启动 - 检查间隔：{CHECK_INTERVAL}秒")
        print(f"📁 日志文件：{self.get_log_file()}")
        print(f"💾 状态文件：{STATE_FILE}")
        
        try:
            while True:
                count = self.run_once()
                if count > 0:
                    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - 检测到 {count} 条新消息")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n👋 监控停止")
            self.save_state()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="飞书消息监控")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--once", action="store_true", help="只运行一次")
    args = parser.parse_args()
    
    watcher = FeishuWatcher()
    
    if args.daemon:
        watcher.run_daemon()
    elif args.once:
        count = watcher.run_once()
        print(f"检测到 {count} 条新消息")
        sys.exit(0 if count == 0 else 1)
    else:
        # 默认守护模式
        watcher.run_daemon()

if __name__ == "__main__":
    main()
