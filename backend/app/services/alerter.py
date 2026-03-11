"""
告警通知服务 - 飞书/钉钉集成
"""
import httpx
import json
from typing import Optional
from datetime import datetime
from app.config import settings


class Alerter:
    """告警通知器"""
    
    def __init__(self):
        self.wechat_webhook = settings.WECHAT_WEBHOOK_URL
        self.dingding_webhook = settings.DINGDING_WEBHOOK_URL
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def send_feishu(self, title: str, content: str, level: str = "info") -> bool:
        """
        发送飞书消息
        """
        if not self.wechat_webhook:
            print("⚠️ 飞书 Webhook 未配置")
            return False
        
        try:
            # 根据告警级别设置颜色
            color_map = {
                "low": "blue",
                "medium": "orange", 
                "high": "red",
                "critical": "red"
            }
            color = color_map.get(level, "blue")
            
            # 构建飞书卡片消息
            payload = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": f"🚨 WaveUP 舆情告警 - {title}"
                        },
                        "template": color
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": content
                        },
                        {
                            "tag": "note",
                            "elements": [
                                {
                                    "tag": "plain_text",
                                    "content": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                }
                            ]
                        }
                    ]
                }
            }
            
            response = await self.client.post(
                self.wechat_webhook,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("StatusCode") == 0:
                    print(f"✅ 飞书告警发送成功：{title}")
                    return True
            
            print(f"❌ 飞书告警发送失败：{response.text}")
            return False
            
        except Exception as e:
            print(f"❌ 飞书告警异常：{e}")
            return False
    
    async def send_dingding(self, title: str, content: str, level: str = "info") -> bool:
        """
        发送钉钉消息
        """
        if not self.dingding_webhook:
            print("⚠️ 钉钉 Webhook 未配置")
            return False
        
        try:
            # 构建钉钉 Markdown 消息
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"WaveUP 舆情告警 - {title}",
                    "text": f"## 🚨 WaveUP 舆情告警\n\n**级别：** {level.upper()}\n\n{content}\n\n⏰ _{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
                },
                "at": {
                    "isAtAll": True  # @所有人
                }
            }
            
            response = await self.client.post(
                self.dingding_webhook,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    print(f"✅ 钉钉告警发送成功：{title}")
                    return True
            
            print(f"❌ 钉钉告警发送失败：{response.text}")
            return False
            
        except Exception as e:
            print(f"❌ 钉钉告警异常：{e}")
            return False
    
    async def send_alert(self, title: str, content: str, level: str = "info", 
                         channel: str = "feishu") -> bool:
        """
        发送告警（自动选择渠道）
        """
        if channel == "feishu":
            return await self.send_feishu(title, content, level)
        elif channel == "dingding":
            return await self.send_dingding(title, content, level)
        else:
            # 默认都发送
            results = await asyncio.gather(
                self.send_feishu(title, content, level),
                self.send_dingding(title, content, level),
                return_exceptions=True
            )
            return any(results)


# 单例
alerter = Alerter()
