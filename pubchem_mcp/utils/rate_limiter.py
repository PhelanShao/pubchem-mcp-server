"""速率限制器实现"""

import time
import asyncio
import logging
from typing import List, Dict
from dataclasses import dataclass, field

logger = logging.getLogger("pubchem-mcp.utils")

@dataclass
class RateLimitStats:
    """速率限制统计信息"""
    total_calls: int = 0
    blocked_calls: int = 0
    total_wait_time: float = 0.0
    last_reset_time: float = field(default_factory=time.time)
    
    def reset(self):
        """重置统计信息"""
        self.total_calls = 0
        self.blocked_calls = 0
        self.total_wait_time = 0.0
        self.last_reset_time = time.time()

class RateLimiter:
    """速率限制器，限制API请求频率"""
    
    def __init__(self, max_calls: int, period: float):
        """
        初始化速率限制器
        
        Args:
            max_calls: 时间段内允许的最大调用次数
            period: 时间段长度(秒)
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []
        self.lock = asyncio.Lock()
        self.stats = RateLimitStats()
    
    async def wait(self):
        """等待，如有必要，以遵守速率限制"""
        async with self.lock:
            now = time.time()
            
            # 清理过期的调用记录
            self.calls = [call_time for call_time in self.calls 
                         if now - call_time < self.period]
            
            # 更新统计信息
            self.stats.total_calls += 1
            
            # 如果达到限制，等待直到最早的调用过期
            if len(self.calls) >= self.max_calls:
                oldest_call = min(self.calls)
                sleep_time = oldest_call + self.period - now
                if sleep_time > 0:
                    self.stats.blocked_calls += 1
                    self.stats.total_wait_time += sleep_time
                    logger.debug(f"速率限制达到，等待 {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
            
            # 记录本次调用
            self.calls.append(time.time())
            
    @property
    def current_calls(self) -> int:
        """获取当前时间段内的调用次数"""
        now = time.time()
        return len([call_time for call_time in self.calls 
                   if now - call_time < self.period])
    
    def get_stats(self) -> Dict:
        """获取速率限制统计信息"""
        now = time.time()
        stats_age = now - self.stats.last_reset_time
        
        return {
            "total_calls": self.stats.total_calls,
            "blocked_calls": self.stats.blocked_calls,
            "total_wait_time": self.stats.total_wait_time,
            "stats_age": stats_age,
            "current_calls": self.current_calls,
            "max_calls": self.max_calls,
            "period": self.period,
            "calls_per_second": self.stats.total_calls / stats_age if stats_age > 0 else 0
        }
    
    def reset_stats(self):
        """重置统计信息"""
        self.stats.reset()