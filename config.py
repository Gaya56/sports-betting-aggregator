"""Configuration settings for the scraper"""

SCRAPER_CONFIG = {
    'rate_limit': {
        'min_delay': 2.0,
        'max_delay': 5.0
    },
    'retry': {
        'max_attempts': 3,
        'backoff_factor': 2
    },
    'timeout': {
        'page_load': 30000,
        'element_wait': 3000
    }
}

URLS = {
    'covers': 'https://www.covers.com/picks',
    'wagertalk': 'https://www.wagertalk.com/free-sports-picks',
    'pickswise': 'https://www.pickswise.com/{sport}/picks',
    'ats': 'https://ats.io/betting-picks/',
    'vegasinsider': 'https://www.vegasinsider.com/picks/'
}

SPORTS = ['nfl', 'nba', 'mlb', 'nhl', 'ncaaf', 'ncaab', 'soccer']