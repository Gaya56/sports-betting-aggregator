# Sports Betting Aggregator

Automated sports betting pick aggregator using AgentQL and AI for web scraping multiple expert sites.

## Features

- Scrapes 5+ major sports betting sites
- AI-powered error handling with OpenAI
- Standardized data format across all sources
- Rate limiting and anti-detection measures
- Modular architecture for easy extension

## Setup

### Prerequisites

- Python 3.8+
- uv package manager
- AgentQL API key
- OpenAI API key (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Gaya56/sports-betting-aggregator.git
cd sports-betting-aggregator
```

2. Install uv if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

5. Set environment variables:
```bash
export AGENTQL_API_KEY="your-agentql-key"
export OPENAI_API_KEY="your-openai-key"  # Optional
```

## Usage

Run the main aggregator:
```bash
uv run python main.py
```

Run specific scraper:
```bash
uv run python -m scrapers.covers_scraper
```

## Project Structure

```
├── scrapers/          # Individual site scrapers
│   ├── base_scraper.py
│   ├── covers_scraper.py
│   ├── wagertalk_scraper.py
│   └── ...
├── utils/             # Helper utilities
│   ├── ai_helper.py
│   ├── data_validator.py
│   └── rate_limiter.py
├── models/            # Data models
│   └── pick_model.py
├── main.py           # Main orchestrator
└── config.py         # Configuration
```

## Output Format

Picks are saved as JSON with this structure:
```json
{
  "expert": "John Doe",
  "sport": "NFL",
  "game": "Cowboys vs Eagles",
  "pick": "Cowboys -3.5",
  "confidence": 0.75,
  "reasoning": "Strong defense...",
  "timestamp": "2025-01-01T12:00:00",
  "source": "Covers"
}
```

## Adding New Scrapers

1. Create new file in `scrapers/`
2. Inherit from `BaseScraper`
3. Implement `get_query()` and `parse_pick_details()`
4. Add to imports in `main.py`

## License

MIT