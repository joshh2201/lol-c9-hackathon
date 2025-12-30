# File Download API Documentation

Complete guide to using the Grid.gg File Download API.

## Base URL

```
https://api.grid.gg/file-download
```

**⚠️ Note:** This is a different base URL from the GraphQL APIs (`api-op.grid.gg`)

## Authentication

Use `x-api-key` header:
```http
x-api-key: your-api-key
```

Or as query parameter:
```
?key=your-api-key
```

## Endpoints

### 1. List Available Files

Get a list of all available files for a series.

**Endpoint:**
```
GET /list/{series_id}
```

**Example:**
```bash
curl -H "x-api-key: YOUR_API_KEY" \
  https://api.grid.gg/file-download/list/2692648
```

**Response:**
```json
{
  "files": [
    {
      "id": "events-grid",
      "description": "Grid Series Events (.jsonl)",
      "status": "ready",
      "fileName": "events_2692648_grid.jsonl.zip",
      "fullURL": "https://api.grid.gg/file-download/events/grid/series/2692648"
    },
    {
      "id": "state-grid",
      "description": "Grid Post Series State (.json)",
      "status": "ready",
      "fileName": "end_state_2692648_grid.json",
      "fullURL": "https://api.grid.gg/file-download/end-state/grid/series/2692648"
    }
  ]
}
```

### 2. Download Events File

Download the zipped Series Events JSONL file (event-by-event data).

**Endpoint:**
```
GET /events/grid/series/{series_id}
```

**Response:**
- Content-Type: `application/zip`
- Binary ZIP file containing JSONL file

**Example:**
```bash
curl -H "x-api-key: YOUR_API_KEY" \
  -o events_2692648.zip \
  https://api.grid.gg/file-download/events/grid/series/2692648
```

### 3. Download End State File

Download the Series End State JSON file (final match state).

**Endpoint:**
```
GET /end-state/grid/series/{series_id}
```

**Response:**
- Content-Type: `application/json`
- JSON file with final series state

**Example:**
```bash
curl -H "x-api-key: YOUR_API_KEY" \
  -o end_state_2692648.json \
  https://api.grid.gg/file-download/end-state/grid/series/2692648
```

## File Status

Files can have different statuses:

| Status | Description | Action |
|--------|-------------|--------|
| `ready` | ✅ File is available for download | Download now |
| `processing` | ⏳ File is being processed | Wait a few minutes |
| `match-not-started` | ⏸️ Series hasn't started | Wait for match to start |
| `match-in-progress` | ▶️ Series is in progress | Wait for match to finish |
| `file-not-available` | ❌ File will not be available | No data for this series |

## File Types

### Events File (`events-grid`)

- **Format:** ZIP containing JSONL (JSON Lines)
- **Content:** Event-by-event data for the entire series
- **Use Case:** Detailed analysis of every event in the match
- **File Name:** `events_{series_id}_grid.jsonl.zip`

**JSONL Format:**
Each line is a JSON object representing an event:
```jsonl
{"timestamp": "2024-01-17T08:05:23Z", "type": "kill", "player": "123", ...}
{"timestamp": "2024-01-17T08:05:45Z", "type": "death", "player": "456", ...}
```

### End State File (`state-grid`)

- **Format:** JSON
- **Content:** Final state of the series (similar to Series State API)
- **Use Case:** Quick access to final match results without API calls
- **File Name:** `end_state_{series_id}_grid.json`

## Usage with Python Script

```bash
# List and download all ready files
python3 file_download_api.py [api-key] [series-id]

# Extract JSONL from events zip
python3 file_download_api.py [api-key] [series-id] --extract

# With .env file
python3 file_download_api.py [series-id]
```

## Workflow

### Step 1: List Files

First, check what files are available:

```python
import requests

series_id = "2692648"
api_key = "your-api-key"

response = requests.get(
    f"https://api.grid.gg/file-download/list/{series_id}",
    headers={"x-api-key": api_key}
)

files = response.json()["files"]
for file_info in files:
    print(f"{file_info['id']}: {file_info['status']}")
```

### Step 2: Download Files

Download files that have status `ready`:

```python
for file_info in files:
    if file_info["status"] == "ready":
        url = file_info["fullURL"]
        response = requests.get(
            url,
            headers={"x-api-key": api_key}
        )
        
        filename = file_info["fileName"]
        with open(filename, "wb") as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
```

### Step 3: Process Events File

Extract and process the JSONL file:

```python
import zipfile
import json

# Extract zip
with zipfile.ZipFile("events_2692648_grid.jsonl.zip", "r") as zip_ref:
    zip_ref.extractall(".")

# Read JSONL
with open("events_2692648_grid.jsonl", "r") as f:
    for line in f:
        event = json.loads(line)
        print(f"Event: {event.get('type')} at {event.get('timestamp')}")
```

## Error Handling

### HTTP Status Codes

- **200 OK** - Success
- **400 Bad Request** - Missing required parameter
- **401 Unauthorized** - Missing or invalid API key
- **403 Forbidden** - No access to this series
- **404 Not Found** - File or series not found
- **5XX** - Server error

### Error Response Format

```json
{
  "message": "Error description"
}
```

## Common Use Cases

1. **Event Analysis**: Download events file to analyze every kill, death, objective, etc.
2. **Offline Processing**: Download files for offline analysis without API rate limits
3. **Data Backup**: Store match data locally
4. **Batch Processing**: Download multiple series files for analysis

## Events File Structure

The JSONL file contains event-by-event data. Common event types include:

- `kill` - Player kill
- `death` - Player death
- `assist` - Kill assist
- `objective` - Objective capture/destruction
- `game_start` - Game started
- `game_end` - Game ended
- `series_start` - Series started
- `series_end` - Series ended

Each event includes:
- `timestamp` - When the event occurred
- `type` - Event type
- `player` / `team` - Who performed the action
- Event-specific data

## Tips

1. **Check Status First**: Always list files first to check status before downloading
2. **Wait for Processing**: If status is `processing`, wait a few minutes and check again
3. **Extract JSONL**: The events file is zipped - extract it to read line-by-line
4. **Stream Processing**: For large files, process JSONL line-by-line instead of loading all into memory

## Next Steps

1. Use Series IDs from `api_explorer.py`
2. Download files with `file_download_api.py`
3. Process events for detailed match analysis
4. Combine with Series State API for complete match data

