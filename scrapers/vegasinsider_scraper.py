from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper
from models.pick_model import Pick

class VegasInsiderScraper(BaseScraper):
    """Scraper for VegasInsider expert picks"""
    
    def __init__(self):
        super().__init__(
            url="https://www.vegasinsider.com/picks/",
            name="VegasInsider"
        )
        
    def get_query(self) -> str:
        return """
        {
            expert_section[] {
                expert_name
                sport
                game_info
                pick_type
                selection
                units_risked
                profit_loss
            }
        }
        """
        
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        picks = []
        
        for item in data.get('expert_section', []):
            try:
                # Higher units = higher confidence
                units = float(item.get('units_risked', '1'))
                confidence = min(0.5 + (units * 0.1), 1.0)
                
                pick = Pick(
                    expert=item.get('expert_name', 'Unknown'),
                    sport=item.get('sport', 'Unknown'),
                    game=item.get('game_info', 'Unknown'),
                    pick=item.get('selection', 'Pending'),
                    confidence=confidence,
                    reasoning=f"{units} units risked",
                    timestamp=datetime.now(),
                    source=self.name
                )
                picks.append(pick)
            except Exception as e:
                self.logger.error(f"Error parsing pick: {e}")
                
        return picks