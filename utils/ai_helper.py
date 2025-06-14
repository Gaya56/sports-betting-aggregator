import os
from typing import Optional
import logging

class AIHelper:
    """Helper for AI-powered query fixing and data cleaning"""
    
    def __init__(self):
        self.logger = logging.getLogger('AIHelper')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                self.logger.warning("OpenAI not installed")
        
    def fix_agentql_query(self, error: str, query: str) -> str:
        """Fix AgentQL syntax errors using AI"""
        if not self.client:
            self.logger.warning("OpenAI client not available")
            return query
            
        prompt = f"""Fix this AgentQL query syntax:
        Error: {error}
        Query: {query}
        
        Return ONLY the corrected query."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"AI query fix failed: {e}")
            return query
        
    def clean_pick_reasoning(self, raw_text: str) -> str:
        """Clean and summarize pick reasoning"""
        cleaned = raw_text.strip()
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        return cleaned
        
    def extract_team_from_pick(self, pick_text: str) -> Optional[str]:
        """Extract team name from pick description"""
        for word in pick_text.split():
            if word.isupper() and len(word) <= 4:
                return word
        return None