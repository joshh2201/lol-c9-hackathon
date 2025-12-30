# Quick Start Guide

## Prerequisites

- Python 3.6+ (already installed on your system)
- API Key from hackathon organizers

## Setup

1. **Get your API Key** from the hackathon organizers

2. **Set your API Key** (choose one method - easiest is Method 1):
   ```bash
   # Method 1: Create .env file (RECOMMENDED - easiest and safest)
   cp env.example .env
   # Then edit .env and add your actual API key
   
   # Method 2: Environment variable
   export GRID_API_KEY="your-api-key-here"
   
   # Method 3: Pass as argument (see usage below)
   ```

## Usage

### Run the API Explorer

```bash
# Easiest: Just run it (reads from .env file automatically)
python3 api_explorer.py

# Or with environment variable
export GRID_API_KEY="your-api-key-here"
python3 api_explorer.py

# Or pass API key directly
python3 api_explorer.py "your-api-key-here"
```

### What the Explorer Does

The script will:
1. ✅ Fetch all available game titles
2. ✅ Get tournaments for a title (defaults to League of Legends / ID "3")
3. ✅ Get all series (matches) for a tournament
4. ✅ Display Series IDs that you can use with other APIs
5. ✅ Explore the API schema to see what's available

## Example Output

Once you have a valid API key, you'll see:

```
📋 Step 1: Fetching available titles...
✅ Found 5 titles

🏆 Step 2: Fetching tournaments for title...
✅ Found 10 tournaments

🎯 Step 3: Fetching series for tournament...
✅ Found 50 series

📝 Sample Series IDs:
  - Series ID: 12345
    Teams: Cloud9 vs Team Liquid
```

## Next Steps

1. **Use Series IDs** with:
   - Series State API - Get match details and state
   - File Download API - Download match data files

2. **Explore More Queries** - Check `API_DOCUMENTATION.md` for:
   - Filtering tournaments by date
   - Getting player information
   - Pagination for large result sets

## Troubleshooting

### SSL Certificate Error
If you see SSL errors, the script will automatically use an unverified context. This is safe for testing.

### Authentication Error
If you see "Requester unauthorized to make query":
- Make sure your API key is correct
- Check that you've set it properly (see Setup above)

### No Data Returned
- Verify your API key has access to the data you're querying
- Check that the title/tournament IDs exist

