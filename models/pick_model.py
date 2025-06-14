from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Pick:
    """Standard data model for sports betting picks"""
    expert: str
    sport: str
    game: str
    pick: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    timestamp: datetime
    source: str = "Unknown"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'expert': self.expert,
            'sport': self.sport,
            'game': self.game,
            'pick': self.pick,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source
        }
        
    def __str__(self) -> str:
        return f"{self.expert}: {self.pick} ({self.confidence:.0%} confident)"