"""
配置管理
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """系统配置"""
    
    # 数据库
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/waveup_sentinel"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API 密钥
    XINBANG_API_KEY: str = ""
    WEIHOT_API_KEY: str = ""
    
    # 告警通知
    WECHAT_WEBHOOK_URL: str = ""
    DINGDING_WEBHOOK_URL: str = ""
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 系统
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置（单例）"""
    return Settings()


settings = get_settings()
