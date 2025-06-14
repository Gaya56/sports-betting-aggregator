#!/usr/bin/env python3
import logging
import json
from datetime import datetime
from typing import List
from scrapers import (
    CoversScraper,
    WagerTalkScraper, 
    PickswiseScraper,
    ATSScraper,
    VegasInsiderScraper
)
from utils import DataValidator
from models import Pick

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def aggregate_picks() -> List[Pick]:
    """Run all scrapers and aggregate picks"""
    all_picks = []
    
    scrapers = [
        CoversScraper(),
        WagerTalkScraper(),
        PickswiseScraper(sport="nfl"),
        ATSScraper(),
        VegasInsiderScraper()
    ]
    
    for scraper in scrapers:
        try:
            picks = scraper.get_picks(headless=False)  # Set True for production
            all_picks.extend(picks)
        except Exception as e:
            logging.error(f"Failed to run {scraper.name}: {e}")
            
    return all_picks

def main():
    """Main orchestrator"""
    logging.info("Starting sports betting pick aggregation")
    
    # Collect all picks
    picks = aggregate_picks()
    
    # Validate and clean
    validator = DataValidator()
    picks = validator.validate_batch(picks)
    picks = validator.check_duplicates(picks)
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file = f"picks_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(
            [pick.to_dict() for pick in picks],
            f,
            indent=2
        )
        
    logging.info(f"Saved {len(picks)} picks to {output_file}")
    
    # Display summary
    print(f"\n{'='*50}")
    print(f"Pick Summary - {timestamp}")
    print(f"{'='*50}")
    for pick in picks[:10]:  # Show first 10
        print(f"{pick}")
    print(f"\nTotal picks collected: {len(picks)}")

if __name__ == "__main__":
    main()