from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper
from models.pick_model import Pick

class CoversScraper(BaseScraper):
    """Scraper for Covers.com expert picks"""
    
    def __init__(self):
        super().__init__(
            url="https://www.covers.com/picks",
            name="Covers"
        )
        
    def get_query(self) -> str:
        return """
        {
            expert_picks[] {
                expert_name
                sport
                game_info
                pick_details
                confidence_rating
            }
        }
        """
        
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        picks = []
        
        for item in data.get('expert_picks', []):
            try:
                pick = Pick(
                    expert=item.get('expert_name', 'Unknown'),
                    sport=item.get('sport', 'Unknown'),
                    game=item.get('game_info', 'Unknown'),
                    pick=item.get('pick_details', 'Pending'),
                    confidence=self.extract_confidence(
                        item.get('confidence_rating', '')
                    ),
                    reasoning="See Covers.com for analysis",
                    timestamp=datetime.now(),
                    source=self.name
                )
                picks.append(pick)
            except Exception as e:
                self.logger.error(f"Error parsing pick: {e}")
                
        return picks