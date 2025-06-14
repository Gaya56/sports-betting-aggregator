from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper
from models.pick_model import Pick

class ATSScraper(BaseScraper):
    """Scraper for ATS.io AI-powered picks"""
    
    def __init__(self):
        super().__init__(
            url="https://ats.io/betting-picks/",
            name="ATS.io"
        )
        
    def get_query(self) -> str:
        return """
        {
            ai_picks[] {
                sport
                game_matchup
                ai_prediction
                confidence_score
                key_factors
                expert_overlay
            }
        }
        """
        
    def parse_pick_details(self, data: Dict) -> List[Pick]:
        picks = []
        
        for item in data.get('ai_picks', []):
            try:
                # Parse confidence as percentage
                conf_text = item.get('confidence_score', '60%')
                confidence = float(conf_text.strip('%')) / 100
                
                pick = Pick(
                    expert="ATS.io AI Model",
                    sport=item.get('sport', 'Unknown'),
                    game=item.get('game_matchup', 'Unknown'),
                    pick=item.get('ai_prediction', 'Pending'),
                    confidence=confidence,
                    reasoning=item.get('key_factors', 'AI analysis'),
                    timestamp=datetime.now(),
                    source=self.name
                )
                picks.append(pick)
            except Exception as e:
                self.logger.error(f"Error parsing pick: {e}")
                
        return picks