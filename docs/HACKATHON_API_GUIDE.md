# Cloud9 x JetBrains Hackathon - Complete API Guide

Based on the official hackathon documentation: [Grid.gg Help Center](https://grid.helpjuice.com/en_US/cloud9-x-jetbrains-hackathon)

## Available APIs

You have access to **three APIs** as part of the hackathon:

1. **Central Data API** - GraphQL API with static data (schedules, teams, etc.)
2. **Series State API** - GraphQL API with post series states (winners, kills, etc.)
3. **File Download API** - REST API to pull event-by-event data files

## Authentication

**⚠️ IMPORTANT:** All APIs use `x-api-key` header authentication (NOT `Authorization: Bearer`)

```http
x-api-key: your-api-key-here
```

## API Endpoints

### 1. Central Data API
- **Endpoint:** `https://api-op.grid.gg/central-data/graphql`
- **Type:** GraphQL
- **Purpose:** Get static data (titles, tournaments, series IDs, teams, players)
- **Documentation:** [Full Documentation](https://portal.grid.gg/documentation/api-documentation/in-game-data/central-data)
- **API Reference:** [API Reference](https://portal.grid.gg/documentation/api-reference/live-data-feed/api-reference-central-data-api)

### 2. Series State API
- **Endpoint:** `https://api-op.grid.gg/live-data-feed/series-state/graphql`
- **Type:** GraphQL
- **Purpose:** Get post-series states (winners, kills, deaths, game results)
- **Documentation:** [Full Documentation](https://portal.grid.gg/documentation/api-documentation/in-game-data/series-state)
- **API Reference:** [API Reference](https://portal.grid.gg/documentation/api-reference/live-data-feed/api-reference-series-state-api)
- **GraphQL Playground:** [GQL Playground](https://docs.grid.gg/public/documentation/graphql-playground)

### 3. File Download API
- **Base URL:** `https://api.grid.gg` ⚠️ **Different base URL!**
- **Type:** REST API
- **Purpose:** Download event-by-event data files (JSONL, JSON)
- **Documentation:** [Full Documentation](https://docs.grid.gg/public/documentation/api-documentation/in-game-data/grid-file-download-api)
- **API Reference:** [API Reference](https://docs.grid.gg/public/documentation/api-reference/live-data-feed/grid-file-download-reference)

## Content Available

### Time Range
- **Past 2 years** of data

### League of Legends Leagues
- LCS (League Championship Series)
- LEC (League of Legends European Championship)
- LCK (League of Legends Champions Korea)
- LPL (League of Legends Pro League)

### Valorant Leagues
- Americas

## Complete Workflow

### Step 1: Get Series IDs from Central Data API

This is where everything starts! Use the Central Data API to get Series IDs.

```graphql
# 1. Get available titles
query Titles {
    titles {
        id
        name
    }
}

# 2. Get tournaments for a title (e.g., League of Legends ID: "3")
query Tournaments {
    tournaments(filter: { title: { id: { in: ["3"] } } }) {
        totalCount
        edges {
            node {
                id
                name
            }
        }
    }
}

# 3. Get series (matches) for a tournament
query AllSeries {
    allSeries(
        filter: { 
            tournament: { 
                id: { in: [756907] }, 
                includeChildren: { equals: true } 
            } 
        }
        orderBy: StartTimeScheduled
    ) {
        totalCount
        edges {
            node {
                id
                startTimeScheduled
                teams {
                    baseInfo {
                        id
                        name
                    }
                }
            }
        }
        pageInfo {
            endCursor
            hasNextPage
        }
    }
}
```

### Step 2: Use Series IDs with Series State API

Once you have a Series ID (e.g., `2692648`), query the Series State API:

**Basic Query:**
```graphql
query SeriesState {
    seriesState(id: "2692648") {
        id
        started
        finished
        teams {
            id
            name
            won
            score
            kills
            deaths
        }
        games {
            id
            sequenceNumber
            map { name }
            teams {
                id
                name
                won
                players {
                    id
                    name
                    kills
                    deaths
                    character { name }
                }
            }
        }
    }
}
```

**League of Legends Enhanced Query (with damage, vision, etc.):**
```graphql
query LoLSeriesState {
    seriesState(id: "2692648") {
        id
        teams {
            id
            name
            score
            won
            ... on SeriesTeamStateLol {
                damageDealt
                damageTaken
                visionScore
                kdaRatio
                totalMoneyEarned
            }
            players {
                id
                name
                kills
                deaths
                ... on SeriesPlayerStateLol {
                    damageDealt
                    visionScore
                    kdaRatio
                    character { name }
                }
            }
        }
    }
}
```

**Request Headers:**
```http
x-api-key: your-api-key-here
Content-Type: application/json
```

**Using the Python Script:**
```bash
python3 series_state_api.py [api-key] [series-id]
# Or with .env file:
python3 series_state_api.py [series-id]
```

See `SERIES_STATE_API_DOCS.md` for complete documentation and all available fields.

### Step 3: Use Series IDs with File Download API

#### Step 3a: Get List of Available Files

First, get the list of available files for a series:

```http
GET https://api.grid.gg/file-download/list/{seriesId}
Headers:
  x-api-key: your-api-key-here
```

**Example:**
```http
GET https://api.grid.gg/file-download/list/2692648
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

**File Statuses:**
- `ready` ✅ - File is available for download
- `processing` ⏳ - File is being processed (wait a few minutes)
- `match-not-started` ⏸️ - Series hasn't started yet
- `match-in-progress` ▶️ - Series is currently playing
- `file-not-available` ❌ - No data available for this series

#### Step 3b: Download Files

Use the `fullURL` from the response to download the file:

```http
GET https://api.grid.gg/file-download/events/grid/series/2692648
Headers:
  x-api-key: your-api-key-here
```

**Available File Types:**
- `events-grid` - Series Events in JSONL format (event-by-event data)
  - ZIP file containing JSONL with every event in the match
  - Use for detailed analysis of kills, deaths, objectives, etc.
- `state-grid` - Post Series State in JSON format (final match state)
  - JSON file with final series state (similar to Series State API)
  - Use for quick access to final results

**Using the Python Script:**
```bash
# List and download all ready files
python3 file_download_api.py [api-key] [series-id]

# Extract JSONL from events zip automatically
python3 file_download_api.py [api-key] [series-id] --extract
```

See `FILE_DOWNLOAD_API_DOCS.md` for complete documentation.

## Testing Your APIs

### GraphQL Playground
- Use the [GQL Playground](https://docs.grid.gg/public/documentation/graphql-playground) to test GraphQL queries
- Or use tools like Postman, Insomnia, Bruno, etc.

### REST API Testing
- Use Postman, Insomnia, Bruno, or curl to test the File Download API

## Example: Complete Workflow

```python
# 1. Get Series ID from Central Data API
series_id = "2692648"

# 2. Query Series State
series_state_query = """
query SeriesState {
    seriesState(id: "2692648") {
        id
        teams { name won }
        games { teams { players { name kills deaths } } }
    }
}
"""

# 3. Get File List
file_list_url = f"https://api.grid.gg/file-download/list/{series_id}"

# 4. Download Events File
events_url = f"https://api.grid.gg/file-download/events/grid/series/{series_id}"
```

## Important Notes

1. **Authentication:** Always use `x-api-key` header, not `Authorization: Bearer`
2. **Base URLs:** File Download API uses `https://api.grid.gg`, others use `https://api-op.grid.gg`
3. **Series IDs:** You must get Series IDs from Central Data API first
4. **Content Limits:** Only past 2 years, specific leagues (LCS, LEC, LCK, LPL for LoL; Americas for Valorant)

## Additional Resources

- **Rate Limits:** [What are the rate limits?](https://grid.helpjuice.com/en_US/client-help/rate-limits-for-products)
- **Pagination:** [How pagination works in GraphQL](https://grid.helpjuice.com/en_US/client-help/how-pagination-works-in-graphql)
- **Live Series:** [Can I get a list of series that are currently live?](https://grid.helpjuice.com/en_US/client-help/can-i-get-a-list-of-series-that-are-currently-live)
- **Rolling Starts:** [How to handle rolling starts in Series Events](https://grid.helpjuice.com/en_US/client-help/how-to-handle-rolling-starts-in-series-events)

## Next Steps

1. ✅ Use `api_explorer.py` to get Series IDs
2. 🔄 Create scripts to query Series State API
3. 🔄 Create scripts to download files from File Download API
4. 🔄 Process and analyze the event data

