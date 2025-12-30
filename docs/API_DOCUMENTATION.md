# Grid.gg Central Data API Documentation

## Overview

The Grid.gg Central Data API is a GraphQL API that provides access to esports data including titles, tournaments, and series information.

**API Endpoint:** `https://api-op.grid.gg/central-data/graphql`

## Authentication

**⚠️ IMPORTANT: This API requires authentication.** You need an API key to access the data.

**Note:** The API uses `x-api-key` header authentication (not `Authorization: Bearer`). See `HACKATHON_API_GUIDE.md` for complete details on all three APIs.

### Setting up API Key

**Option 1: .env File (Recommended - Easiest)**
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API key:
# GRID_API_KEY=your-api-key-here

# Then just run (it reads .env automatically)
python3 api_explorer.py
```

**Option 2: Environment Variable**
```bash
export GRID_API_KEY="your-api-key-here"
python3 api_explorer.py
```

**Option 3: Command Line Argument**
```bash
python3 api_explorer.py "your-api-key-here"
```

**Option 4: Direct Header (in code)**
```
Authorization: Bearer your-api-key-here
```

**Note:** The `.env` file is gitignored and won't be committed to version control, making it safe for storing your API key locally.

### Getting an API Key

Contact the hackathon organizers or check the hackathon documentation for how to obtain your API key.

## Quick Start Workflow

### Step 1: Get Available Titles

Query to get all available game titles:

```graphql
query Titles {
    titles {
        id
        name
    }
}
```

**Response Example:**
```json
{
    "data": {
        "titles": [
            {
                "id": "3",
                "name": "League of Legends"
            }
        ]
    }
}
```

### Step 2: Get Tournaments for a Title

Query tournaments for a specific title (using title ID from Step 1):

```graphql
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
```

**Response Example:**
```json
{
    "data": {
        "tournaments": {
            "totalCount": 10,
            "edges": [
                {
                    "node": {
                        "id": "756907",
                        "name": "LCS Spring 2024"
                    }
                }
            ]
        }
    }
}
```

### Step 3: Get Series for a Tournament

Query all series (matches) for a tournament:

```graphql
query AllSeries {
    allSeries(
        filter: { tournament: { id: { in: [756907] }, includeChildren: { equals: true } } }
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

**Response Example:**
```json
{
    "data": {
        "allSeries": {
            "totalCount": 50,
            "edges": [
                {
                    "node": {
                        "id": "12345",
                        "startTimeScheduled": "2024-01-15T10:00:00Z",
                        "teams": [
                            {
                                "baseInfo": {
                                    "id": "100",
                                    "name": "Cloud9"
                                }
                            },
                            {
                                "baseInfo": {
                                    "id": "200",
                                    "name": "Team Liquid"
                                }
                            }
                        ]
                    }
                }
            ],
            "pageInfo": {
                "endCursor": "cursor123",
                "hasNextPage": true
            }
        }
    }
}
```

## Using Series IDs

Once you have Series IDs from the `allSeries` query, you can use them with:

1. **Series State API** - Get real-time or historical state of a series
2. **File Download API** - Download match data files

## Available Query Fields

The API supports various query fields. Common ones include:

- `titles` - Get all game titles
- `tournaments` - Get tournaments with filtering
- `allSeries` - Get series/matches with filtering and pagination
- `series` - Get individual series information
- `teams` - Get team information
- `players` - Get player information

## Filtering and Pagination

### Filtering Tournaments
```graphql
tournaments(filter: { 
    title: { id: { in: ["3"] } }
    # Add more filters as needed
})
```

### Filtering Series
```graphql
allSeries(
    filter: { 
        tournament: { 
            id: { in: [756907] }, 
            includeChildren: { equals: true } 
        }
    }
    orderBy: StartTimeScheduled
)
```

### Pagination
Series queries support cursor-based pagination:
- Use `pageInfo.endCursor` to get the next page
- Check `pageInfo.hasNextPage` to see if more data is available
- Pass `after: "cursor"` parameter for subsequent queries

## Error Handling

### Common Errors

**UNAUTHENTICATED Error:**
```json
{
  "errors": [
    {
      "message": "Requester unauthorized to make query",
      "extensions": {
        "errorType": "UNAUTHENTICATED"
      }
    }
  ]
}
```
**Solution:** You need to provide a valid API key. See Authentication section above.

### HTTP Status Codes
- `200` - Success
- `401` - Unauthorized (missing or invalid API key)
- `403` - Forbidden (insufficient permissions)
- `400` - Bad Request (invalid query)
- `500` - Server Error

### SSL Certificate Issues

If you encounter SSL certificate verification errors on macOS, the script will automatically fall back to an unverified context. This is safe for testing but you may want to install Python certificates properly for production use.

## Next Steps

1. Use Series IDs with the Series State API to get match details
2. Use Series IDs with the File Download API to download match data
3. Explore additional query fields for players, stats, etc.

## Complete API Reference

For the complete API reference including all queries, mutations, objects, inputs, and enums, see **`CENTRAL_DATA_API_REFERENCE.md`**.

The complete reference includes:
- All available queries (players, teams, organizations, content catalog, etc.)
- All mutations (create/update/delete operations)
- Complete object definitions with all fields
- Filter inputs and enums
- Common query patterns
- Pagination examples

