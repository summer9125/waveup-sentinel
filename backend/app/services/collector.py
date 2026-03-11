"""
数据采集服务 - 对接第三方 API
"""
import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from app.config import settings


class DataCollector:
    """数据采集器"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.xinbang_api_key = settings.XINBANG_API_KEY
        self.weihot_api_key = settings.WEIHOT_API_KEY
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
    
    async def collect_from_xinbang(self, keywords: List[str], limit: int = 50) -> List[Dict]:
        """
        从新榜采集数据
        支持：公众号、抖音、快手等
        
        API 文档：https://api.newrank.cn/docs
        """
        if not self.xinbang_api_key:
            print("⚠️ 新榜 API 密钥未配置")
            return []
        
        results = []
        headers = {"Authorization": f"Bearer {self.xinbang_api_key}"}
        
        for keyword in keywords:
            try:
                # 新榜公众号文章搜索 API
                url = "https://api.newrank.cn/v1/wechat/article/search"
                params = {
                    "keyword": keyword,
                    "limit": limit,
                    "page": 1
                }
                
                response = await self.client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200:
                        articles = data.get("data", {}).get("list", [])
                        for article in articles:
                            results.append({
                                "platform": "wechat",
                                "event_type": "article",
                                "title": article.get("title", ""),
                                "content": article.get("digest", ""),
                                "author": article.get("author", ""),
                                "publish_time": article.get("publish_time", ""),
                                "url": article.get("url", ""),
                                "view_count": article.get("read_count", 0),
                                "like_count": article.get("like_count", 0),
                                "raw_data": article
                            })
                        print(f"✅ 从新榜采集：{keyword} - {len(articles)} 篇文章")
                    else:
                        print(f"❌ 新榜 API 错误：{data.get('msg', 'Unknown error')}")
                else:
                    print(f"❌ 新榜 API 请求失败：{response.status_code}")
                
            except Exception as e:
                print(f"❌ 新榜采集失败 {keyword}: {e}")
        
        return results
    
    async def collect_from_weihot(self, keywords: List[str], limit: int = 50) -> List[Dict]:
        """
        从微热点采集数据
        支持：微博、微信、抖音等全网数据
        """
        if not self.weihot_api_key:
            print("⚠️ 微热点 API 密钥未配置")
            return []
        
        results = []
        
        for keyword in keywords:
            try:
                # 模拟 API 调用
                print(f"🔥 从微热点采集：{keyword}")
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ 微热点采集失败 {keyword}: {e}")
        
        return results
    
    async def collect_manual(self, platform: str, url: str) -> Optional[Dict]:
        """
        手动录入舆情事件
        用于无法自动采集的平台（如视频号）
        """
        # TODO: 实现手动录入逻辑
        return {
            "platform": platform,
            "url": url,
            "collected_at": datetime.now()
        }
    
    async def collect_all(self, keywords: List[str]) -> List[Dict]:
        """
        从所有数据源采集
        """
        tasks = [
            self.collect_from_xinbang(keywords),
            self.collect_from_weihot(keywords)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 合并结果
        all_data = []
        for result in results:
            if isinstance(result, list):
                all_data.extend(result)
        
        return all_data


# 单例
collector = DataCollector()
