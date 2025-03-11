"""内存缓存实现"""

import time
from typing import Optional, Any, Dict

class MemoryCache:
    """简单的内存缓存系统"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 24*60*60):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl: 缓存生存时间(秒)
        """
        self.cache: Dict[str, tuple] = {}
        self.max_size = max_size
        self.ttl = ttl
        
    async def get(self, key: str) -> Optional[Any]:
        """从缓存获取值"""
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl:
            # 缓存已过期
            del self.cache[key]
            return None
            
        return value
    
    async def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        # 如果缓存已满，移除最旧的项
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    async def get_or_set(self, key: str, value_func) -> Any:
        """获取缓存值，如果不存在则设置"""
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        value = await value_func()
        await self.set(key, value)
        return value
        
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        
    def remove(self, key: str) -> None:
        """移除缓存项"""
        if key in self.cache:
            del self.cache[key]
            
    @property
    def size(self) -> int:
        """获取当前缓存大小"""
        return len(self.cache)
        
    @property
    def stats(self) -> Dict:
        """获取缓存统计信息"""
        now = time.time()
        active_items = len([1 for _, (_, ts) in self.cache.items() 
                          if now - ts <= self.ttl])
        return {
            "total_items": len(self.cache),
            "active_items": active_items,
            "expired_items": len(self.cache) - active_items,
            "max_size": self.max_size,
            "ttl": self.ttl
        }