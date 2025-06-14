from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper
from models.pick_model import Pick

class PickswiseScraper(BaseScraper):
    """Scraper for Pickswise predictions"""
    
    def __init__(self, sport="nfl"):
        self.sport = sport
        super().__init__(
            url=f"https://www.pickswise.com/{sport}/picks",
            name="Pickswise"
        )
        
    def get_query(self) -> str:
        return """
        {
            game_picks[] {
                teams
                expert_pick
                star_rating
                prediction_type
                reasoning_summary
                game_time
            }
        }
        """
        
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        picks = []
        
        for item in data.get('game_picks', []):
            try:
                pick = Pick(
                    expert="Pickswise Team",
                    sport=self.sport.upper(),
                    game=item.get('teams', 'Unknown'),
                    pick=item.get('expert_pick', 'Pending'),
                    confidence=self.extract_confidence(
                        item.get('star_rating', '')
                    ),
                    reasoning=item.get('reasoning_summary', 'See full analysis'),
                    timestamp=datetime.now(),
                    source=self.name
                )
                picks.append(pick)
            except Exception as e:
                self.logger.error(f"Error parsing pick: {e}")
                
        return picks