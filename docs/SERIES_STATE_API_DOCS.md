# Series State API Documentation

Complete guide to using the Grid.gg Series State API based on the official API reference.

## Endpoint

```
https://api-op.grid.gg/live-data-feed/series-state/graphql
```

## Authentication

Use `x-api-key` header:
```http
x-api-key: your-api-key
```

## Queries

### 1. `seriesState(id: ID!)`

Get the complete state of a series (match) by Series ID.

**Example Query:**
```graphql
query SeriesState {
    seriesState(id: "2692648") {
        id
        version
        title {
            nameShortened
        }
        format
        started
        finished
        teams {
            id
            name
            score
            won
            kills
            deaths
        }
        games {
            id
            sequenceNumber
            started
            finished
            map {
                name
            }
            teams {
                id
                name
                side
                won
                score
            }
        }
    }
}
```

### 2. `latestSeriesStateByPlayerId(id: ID!)`

Get the latest series that a player participated in.

**Example Query:**
```graphql
query LatestSeriesByPlayer {
    latestSeriesStateByPlayerId(id: "12345") {
        id
        title {
            nameShortened
        }
        format
        teams {
            id
            name
            score
            won
        }
    }
}
```

## Key Objects

### SeriesState

Main object containing all series information.

**Core Fields:**
- `id` - Series ID
- `version` - Data model version
- `title` - Esports title (e.g., League of Legends)
- `format` - Series format (e.g., "Best of 3")
- `started` / `finished` - Status booleans
- `startedAt` - When series started
- `duration` - Total duration
- `teams` - List of teams
- `games` - List of games in the series

### SeriesTeamState (League of Legends)

Team-level statistics for the entire series.

**Common Fields:**
- `id`, `name`, `score`, `won`
- `kills`, `deaths`
- `killsAndAssists` - Sum of kills and assists

**League of Legends Specific:**
- `damageDealt` / `damageTaken` - Total damage
- `visionScore` - Vision control score
- `kdaRatio` - KDA ratio
- `totalMoneyEarned` - Total gold earned
- `baronPowerPlays` - Baron buff plays completed
- `moneyPerMinute` - Gold per minute
- `damagePerMinute` - Damage per minute

### SeriesPlayerState (League of Legends)

Player-level statistics for the entire series.

**Common Fields:**
- `id`, `name`
- `kills`, `deaths`, `killAssistsGiven`
- `character` - Champion played

**League of Legends Specific:**
- `damageDealt` / `damageTaken`
- `damagePercentage` - % of team's total damage
- `visionScore` / `visionScorePerMinute`
- `kdaRatio`
- `totalMoneyEarned` / `moneyPerMinute`
- `killParticipation` - % of team kills participated in
- `forwardPercentage` - Time spent on enemy side of map

### GameState

Individual game within a series.

**Fields:**
- `id`, `sequenceNumber`
- `started` / `finished`
- `startedAt`, `duration`
- `map` - Map information
- `teams` - Teams in this game
- `clock` - Game clock state

### GameTeamState / GamePlayerState

Similar to Series-level but for individual games.

**GamePlayerStateLol Additional Fields:**
- `respawnClock` - When player respawns
- `currentHealth` / `maxHealth`
- `alive` - Is player alive
- `position` - Player coordinates

## Example: Complete League of Legends Query

```graphql
query FullLoLSeriesState {
    seriesState(id: "2692648") {
        id
        version
        title {
            nameShortened
        }
        format
        started
        finished
        startedAt
        duration
        teams {
            id
            name
            score
            won
            kills
            deaths
            ... on SeriesTeamStateLol {
                damageDealt
                damageTaken
                visionScore
                kdaRatio
                totalMoneyEarned
                moneyPerMinute
                baronPowerPlays {
                    id
                    value
                }
            }
            players {
                id
                name
                kills
                deaths
                killAssistsGiven
                character {
                    id
                    name
                }
                ... on SeriesPlayerStateLol {
                    damageDealt
                    damageTaken
                    damagePercentage
                    visionScore
                    visionScorePerMinute
                    kdaRatio
                    totalMoneyEarned
                    moneyPerMinute
                    damagePerMinute
                    killParticipation
                    forwardPercentage
                }
            }
        }
        games {
            id
            sequenceNumber
            started
            finished
            startedAt
            duration
            map {
                name
            }
            teams {
                id
                name
                side
                won
                score
                kills
                deaths
                ... on GameTeamStateLol {
                    damageDealt
                    damageTaken
                    visionScore
                }
                players {
                    id
                    name
                    kills
                    deaths
                    character {
                        id
                        name
                    }
                    ... on GamePlayerStateLol {
                        damageDealt
                        damageTaken
                        damagePercentage
                        visionScore
                        kdaRatio
                        totalMoneyEarned
                        respawnClock {
                            ticking
                            currentSeconds
                        }
                    }
                }
            }
        }
    }
}
```

## Usage with Python Script

```bash
# Basic usage
python3 series_state_api.py [api-key] [series-id]

# With .env file
python3 series_state_api.py

# Save full JSON output
python3 series_state_api.py [api-key] [series-id] --save-json
```

## Available Data by Game Type

The API provides game-specific fields:

- **League of Legends**: Damage stats, vision score, gold, KDA, baron plays
- **CS2/CSGO**: Money, loadout value, armor, headshots
- **Valorant**: Abilities, ultimate points, armor
- **Dota 2**: Experience points, kill streaks
- **PUBG**: Headshots, knockdowns
- **R6**: Healing, knockdowns

Use fragments (`... on GamePlayerStateLol`) to access game-specific fields.

## Common Use Cases

1. **Match Results**: Get winner, scores, game-by-game breakdown
2. **Player Stats**: KDA, damage, vision score, gold earned
3. **Team Performance**: Team damage, vision control, gold leads
4. **Game Analysis**: Map-by-map performance, game duration
5. **Champion Stats**: Character performance across games

## Error Handling

The API returns errors in standard GraphQL format:
```json
{
  "errors": [
    {
      "message": "Error message",
      "extensions": {
        "errorType": "NOT_FOUND"
      }
    }
  ]
}
```

Common error types:
- `NOT_FOUND` - Series ID doesn't exist
- `UNAUTHENTICATED` - Invalid API key
- `BAD_REQUEST` - Invalid query

## Next Steps

1. Use Series IDs from `api_explorer.py` to query match data
2. Analyze player performance across multiple series
3. Build dashboards with team/player statistics
4. Track champion performance and win rates

