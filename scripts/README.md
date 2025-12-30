# Scripts Directory

Python scripts for interacting with Grid.gg APIs.

## Scripts

- **`api_explorer.py`** - Explore Central Data API, get Series IDs
- **`series_state_api.py`** - Query Series State API for match stats
- **`file_download_api.py`** - Download event-by-event data files
- **`data_explorer.py`** - Comprehensive data exploration
- **`query_available_data.py`** - Test what data is available
- **`get_valorant_series.py`** - Get random Valorant Americas series

## Usage

All scripts can be run from the project root:

```bash
python3 scripts/api_explorer.py
python3 scripts/series_state_api.py [api-key] [series-id]
```

Or from this directory:

```bash
cd scripts
python3 api_explorer.py
```

## API Key

Scripts automatically read your API key in this priority order:
1. **`.env` file** (project root) - **Recommended!** ⭐
2. `GRID_API_KEY` environment variable
3. Command line argument (override/fallback)

**Setup:**
```bash
# Create .env file in project root
cp ../env.example ../.env

# Edit .env and add your key:
GRID_API_KEY=your-api-key-here
```

Once set up, you can run scripts without passing the API key:
```bash
python3 api_explorer.py
python3 series_state_api.py 2654004
```

