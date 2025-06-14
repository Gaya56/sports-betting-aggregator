from typing import List, Dict
import logging
from models.pick_model import Pick

class DataValidator:
    """Validate scraped pick data"""
    
    def __init__(self):
        self.logger = logging.getLogger('DataValidator')
        
    def validate_pick(self, pick: Pick) -> bool:
        """Validate single pick has required fields"""
        required = ['expert', 'sport', 'game', 'pick']
        
        for field in required:
            if not getattr(pick, field, None):
                self.logger.warning(f"Missing required field: {field}")
                return False
                
        if not 0 <= pick.confidence <= 1:
            self.logger.warning(f"Invalid confidence: {pick.confidence}")
            return False
            
        return True
        
    def validate_batch(self, picks: List[Pick]) -> List[Pick]:
        """Validate and filter list of picks"""
        valid_picks = []
        
        for pick in picks:
            if self.validate_pick(pick):
                valid_picks.append(pick)
            else:
                self.logger.warning(f"Rejecting invalid pick from {pick.expert}")
                
        return valid_picks
        
    def check_duplicates(self, picks: List[Pick]) -> List[Pick]:
        """Remove duplicate picks"""
        seen = set()
        unique = []
        
        for pick in picks:
            key = f"{pick.expert}_{pick.game}_{pick.pick}"
            if key not in seen:
                seen.add(key)
                unique.append(pick)
                
        return unique