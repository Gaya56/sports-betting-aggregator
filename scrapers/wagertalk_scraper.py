from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper
from models.pick_model import Pick

class WagerTalkScraper(BaseScraper):
    """Scraper for WagerTalk free picks"""
    
    def __init__(self):
        super().__init__(
            url="https://www.wagertalk.com/free-sports-picks",
            name="WagerTalk"
        )
        
    def get_query(self) -> str:
        return """
        {
            pick_table[] {
                handicapper_name
                sport
                matchup
                pick_selection
                win_percentage
                analysis_link
            }
        }
        """
        
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        picks = []
        
        for item in data.get('pick_table', []):
            try:
                # Convert win percentage to confidence
                win_pct = item.get('win_percentage', '50%')
                confidence = float(win_pct.strip('%')) / 100
                
                pick = Pick(
                    expert=item.get('handicapper_name', 'Unknown'),
                    sport=item.get('sport', 'Unknown'), 
                    game=item.get('matchup', 'Unknown'),
                    pick=item.get('pick_selection', 'Pending'),
                    confidence=confidence,
                    reasoning="Full analysis on WagerTalk",
                    timestamp=datetime.now(),
                    source=self.name
                )
                picks.append(pick)
            except Exception as e:
                self.logger.error(f"Error parsing pick: {e}")
                
        return picks