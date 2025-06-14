import time
import random
from typing import List

class RateLimiter:
    """Rate limiting and user agent rotation"""
    
    def __init__(self, min_delay: float = 2.0, max_delay: float = 5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0"
        ]
        
    def wait(self):
        """Apply random delay between requests"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        
    def get_random_user_agent(self) -> str:
        """Get random user agent string"""
        return random.choice(self.user_agents)