"""
免费数据采集服务 - 使用公开数据源
"""
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import asyncio

class FreeDataCollector:
    """免费数据采集器"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            headers={"User-Agent": "Mozilla/5.0 (WaveUP Sentinel)"}
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def get_weibo_hot(self) -> List[Dict]:
        """获取微博热搜（免费）"""
        try:
            # 使用公开的微博热搜 API
            url = "https://weibo.com/ajax/side/hotSearch"
            resp = await self.client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                hot_list = data.get('data', {}).get('realtime', [])[:20]
                return [
                    {
                        "title": item.get('note', ''),
                        "position": item.get('position', 0),
                        "hot_value": item.get('num', 0),
                        "source": "weibo",
                        "url": f"https://s.weibo.com/weibo?q={item.get('note', '')}",
                        "collected_at": datetime.now().isoformat()
                    }
                    for item in hot_list if item.get('note')
                ]
        except Exception as e:
            print(f"微博热搜获取失败：{e}")
        return []
    
    async def get_baidu_news(self, keyword: str = "热点") -> List[Dict]:
        """获取百度新闻（免费 RSS）"""
        try:
            url = f"http://news.baidu.com/ns?word={keyword}&tn=news&from=news&cl=2&ct=1&si=&rn=20"
            resp = await self.client.get(url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'lxml')
                results = soup.find_all('div', class_='result-op')[:20]
                return [
                    {
                        "title": item.find('h3').text.strip() if item.find('h3') else "",
                        "summary": item.find('p', class_='c-summary').text.strip() if item.find('p', class_='c-summary') else "",
                        "source": "baidu_news",
                        "url": item.find('a')['href'] if item.find('a') else "",
                        "collected_at": datetime.now().isoformat()
                    }
                    for item in results if item.find('h3')
                ]
        except Exception as e:
            print(f"百度新闻获取失败：{e}")
        return []
    
    async def get_zhihu_hot(self) -> List[Dict]:
        """获取知乎热榜（免费）"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20&desktop=true"
            resp = await self.client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "title": item.get('target', {}).get('title', ''),
                        "summary": item.get('target', {}).get('excerpt', ''),
                        "hot_value": item.get('children', [{}])[0].get('vote_count', 0),
                        "source": "zhihu",
                        "url": f"https://www.zhihu.com/question/{item.get('target', {}).get('id', '')}",
                        "collected_at": datetime.now().isoformat()
                    }
                    for item in data.get('data', [])
                ]
        except Exception as e:
            print(f"知乎热榜获取失败：{e}")
        return []
    
    async def collect_all(self) -> Dict:
        """采集所有免费数据源"""
        tasks = [
            self.get_weibo_hot(),
            self.get_baidu_news(),
            self.get_zhihu_hot()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "weibo": results[0] if isinstance(results[0], list) else [],
            "baidu_news": results[1] if isinstance(results[1], list) else [],
            "zhihu": results[2] if isinstance(results[2], list) else [],
            "collected_at": datetime.now().isoformat()
        }


collector = FreeDataCollector()
