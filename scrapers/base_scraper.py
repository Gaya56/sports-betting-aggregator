from abc import ABC, abstractmethod
from datetime import datetime
import logging
import agentql
from playwright.sync_api import sync_playwright
from typing import List, Dict, Optional
from utils.rate_limiter import RateLimiter
from models.pick_model import Pick

class BaseScraper(ABC):
    """Abstract base class for all sports betting scrapers"""
    
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.logger = logging.getLogger(name)
        self.rate_limiter = RateLimiter()
        
    @abstractmethod
    def get_query(self) -> str:
        """Return AgentQL query for this scraper"""
        pass
        
    @abstractmethod
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        """Parse raw data into Pick objects"""
        pass
    
    def get_picks(self, headless: bool = True) -> List[Pick]:
        """Main entry point for scraping"""
        self.logger.info(f"Starting {self.name} scraper")
        
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=headless)
                page = agentql.wrap(browser.new_page())
                
                # Apply rate limiting
                self.rate_limiter.wait()
                
                # Navigate and scrape
                page.goto(self.url)
                page.wait_for_timeout(3000)
                
                data = page.query_data(self.get_query())
                picks = self.parse_pick_details(data)
                
                browser.close()
                
                self.logger.info(f"Found {len(picks)} picks from {self.name}")
                return picks
                
        except Exception as e:
            self.logger.error(f"Error scraping {self.name}: {e}")
            return []
            
    def extract_confidence(self, text: str) -> float:
        """Extract confidence score from text (0.0-1.0)"""
        if "★★★" in text or "3 star" in text.lower():
            return 0.9
        elif "★★" in text or "2 star" in text.lower():
            return 0.7
        elif "★" in text or "1 star" in text.lower():
            return 0.5
        return 0.6  # default