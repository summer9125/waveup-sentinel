"""
情感分析服务
"""
from snownlp import SnowNLP
from typing import Dict, Optional


class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        pass
    
    def analyze(self, text: str) -> Dict:
        """
        分析文本情感
        
        返回：
        {
            "score": 0.85,        # 情感得分 0-1，越接近 1 越正面
            "label": "positive",  # positive/negative/neutral
            "confidence": 0.92    # 置信度
        }
        """
        if not text:
            return {
                "score": 0.5,
                "label": "neutral",
                "confidence": 0.0
            }
        
        # 使用 SnowNLP 进行中文情感分析
        s = SnowNLP(text)
        score = s.sentiments  # 0-1 之间的浮点数
        
        # 转换为 -1 到 1 的范围
        normalized_score = (score * 2) - 1
        
        # 判断情感标签
        if score > 0.6:
            label = "positive"
            confidence = score
        elif score < 0.4:
            label = "negative"
            confidence = 1 - score
        else:
            label = "neutral"
            confidence = 1 - abs(score - 0.5) * 2
        
        return {
            "score": round(normalized_score, 2),
            "label": label,
            "confidence": round(confidence, 2)
        }
    
    def analyze_batch(self, texts: list) -> list:
        """批量分析"""
        return [self.analyze(text) for text in texts]


# 单例
analyzer = SentimentAnalyzer()
