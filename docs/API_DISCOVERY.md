# API Discovery Results

## ✅ API Connection Status
**Status:** Working with API key authentication

## Available Data

### Titles (Games)
Found **38 titles** including:
- League of Legends (ID: 3)
- Counter Strike: Global Offensive (ID: 1)
- Valorant (ID: 6)
- Defense of the Ancients 2 (ID: 2)
- And 34 more titles

### League of Legends Tournaments
Found **173 tournaments** for League of Legends, including:
- LCK - Spring 2024 (Regular Season) - ID: 756907
- LEC - Winter 2024 (Regular Season) - ID: 756928
- LCS - Spring 2024 (Regular Season) - ID: 756935
- LPL - Spring 2024 (Regular Season) - ID: 756960
- And many more...

### Series (Matches)
Example tournament (LCK Spring 2024 - ID: 756907) has **90 series** including:

| Series ID | Teams | Scheduled Time |
|-----------|-------|----------------|
| 2616371 | NONGSHIM RED FORCE vs DRX | 2024-01-17T08:00:00Z |
| 2616372 | T1 vs Gen.G Esports | 2024-01-17T11:00:00Z |
| 2616373 | OKSavingsBank BRION vs Dplus KIA | 2024-01-18T08:00:00Z |
| 2616374 | BNK FearX vs KT Rolster | 2024-01-18T10:50:00Z |
| 2616375 | Hanwha Life Esports vs DRX | 2024-01-19T08:00:00Z |

## Available Query Fields

The API provides access to:

### Core Entities
- `title` / `titles` - Game titles
- `tournament` / `tournaments` - Tournaments
- `series` / `allSeries` - Match series
- `team` / `teams` - Teams
- `player` / `players` - Players
- `organization` / `organizations` - Organizations

### Lookup Functions
- `tournamentIdByExternalId` - Find tournament by external ID
- `teamIdByExternalId` - Find team by external ID
- `seriesIdByExternalId` - Find series by external ID
- `playerIdByExternalId` - Find player by external ID
- `gameIdByExternalId` - Find game by external ID

### Additional Data
- `seriesFormats` - Series format information
- `dataProviders` - Data provider information
- `playerRole` / `playerRoles` - Player role information

## Next Steps

### Using Series IDs
Now that we have Series IDs (like `2616371`, `2616372`, etc.), you can:

1. **Series State API** - Get real-time or historical match state
   - Use Series ID to query match details, scores, events, etc.

2. **File Download API** - Download match data files
   - Use Series ID to download replay files, telemetry data, etc.

### Example Series IDs to Try
- `2616371` - NONGSHIM RED FORCE vs DRX
- `2616372` - T1 vs Gen.G Esports (popular match!)
- `2616373` - OKSavingsBank BRION vs Dplus KIA

## Pagination

The API supports cursor-based pagination:
- Use `pageInfo.endCursor` to get the next page
- Check `pageInfo.hasNextPage` to see if more data exists
- Pass `after: "cursor"` parameter for subsequent queries

## Authentication

✅ API key authentication is working
- Format: `Authorization: Bearer {key}` or `X-API-Key: {key}`
- Both headers are sent for compatibility

