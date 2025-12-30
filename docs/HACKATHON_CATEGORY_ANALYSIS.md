# Hackathon Category Data Analysis

Analysis of available GRID API data for each hackathon category.

## Available APIs Summary

1. **Central Data API** - Static data (teams, players, series metadata, content catalog)
2. **Series State API** - Match statistics (KDA, damage, vision, gold, draft actions)
3. **File Download API** - Event-by-event data (JSONL files with every game event)

---

## Category 1: Assistant Coach (Micro + Macro Analytics)

**Goal:** Merge micro-level player analytics with macro-level strategic review to identify mistakes and their team impact.

### ✅ Available Data

#### Micro-Level (Individual Player Analytics)

**From Series State API:**
- **KDA Metrics:**
  - `kills`, `deaths`, `killAssistsGiven` - Per game and per series
  - `kdaRatio` - KDA ratio calculation
  - `killParticipation` - % of team kills participated in
  - `firstKill` - First blood acquisition

- **Damage Metrics:**
  - `damageDealt` - Total damage dealt
  - `damageTaken` - Total damage taken
  - `damagePercentage` - % of team's total damage
  - `damagePerMinute` - Damage efficiency metric
  - `damagePerMoney` - Damage per gold earned

- **Vision Metrics:**
  - `visionScore` - Total vision score
  - `visionScorePerMinute` - Vision efficiency

- **Gold/Economy Metrics:**
  - `totalMoneyEarned` - Total gold earned
  - `moneyPerMinute` - Gold per minute
  - `moneyPercentage` - % of team's total gold
  - `netWorth` - Current net worth

- **Positioning:**
  - `forwardPercentage` - Time spent on enemy side of map
  - `position` - Player coordinates (game-level)

- **Champion Performance:**
  - `character` - Champion played
  - Champion-specific stats per game

- **Game State:**
  - `respawnClock` - Respawn timing
  - `alive` - Current alive status
  - `currentHealth` / `maxHealth`

#### Macro-Level (Team Strategy)

**From Series State API:**
- **Team Aggregates:**
  - `damageDealt` / `damageTaken` - Team damage
  - `visionScore` - Team vision control
  - `kdaRatio` - Team KDA
  - `totalMoneyEarned` - Team economy
  - `baronPowerPlays` - Baron buff utilization

- **Game Outcomes:**
  - `won` - Win/loss per game and series
  - `score` - Game scores
  - `duration` - Game and series duration
  - `map` - Map played

- **Team Composition:**
  - Champion selections per game
  - Team synergy data

**From Central Data API:**
- Series metadata (format, tournament, date)
- Team information (ratings, organization)
- Player roles and positions

**From File Download API:**
- **Event-by-Event Data:**
  - Every kill, death, assist
  - Objective captures/destructions
  - Item purchases
  - Ability usage
  - Position changes over time
  - Exact timestamps for all events

### 🔍 Use Cases for Category 1

1. **Mistake Identification:**
   - Low vision score → Team vision gaps
   - High deaths → Positioning issues
   - Low damage percentage → Inefficient resource usage
   - High forward percentage + high deaths → Over-aggression

2. **Pattern Recognition:**
   - Recurring mistakes across multiple games
   - Performance degradation over time
   - Champion-specific weaknesses

3. **Impact Analysis:**
   - Connect individual mistakes to team losses
   - Identify critical moments where mistakes occurred
   - Correlate micro mistakes with macro game state

4. **Actionable Insights:**
   - "Player X has 40% higher death rate when playing on red side"
   - "Team loses 80% of games when vision score drops below threshold"
   - "Player Y's damage drops 30% in games 2-3 of series (fatigue indicator)"

### 📊 Data Queries Needed

```graphql
# Get player performance across multiple series
query PlayerHistory {
    allSeries(
        filter: {
            players: {
                # Filter by specific player
            }
        }
        orderBy: StartTimeScheduled
    ) {
        edges {
            node {
                id
                startTimeScheduled
                # Then query Series State API for each series
            }
        }
    }
}

# Get comprehensive player stats
query PlayerStats {
    seriesState(id: "series-id") {
        teams {
            players {
                ... on SeriesPlayerStateLol {
                    kills
                    deaths
                    damageDealt
                    visionScore
                    # All micro metrics
                }
            }
            ... on SeriesTeamStateLol {
                # All macro metrics
            }
        }
    }
}
```

---

## Category 2: Automated Scouting Report Generator

**Goal:** Generate scouting reports for upcoming opponents based on recent match data.

### ✅ Available Data

#### Opponent Team Information

**From Central Data API:**
- Team name, logo, colors
- Team rating
- Organization affiliation
- Recent series participation
- Tournament history

#### Recent Match History

**From Central Data API:**
```graphql
# Get all recent series for a team
query OpponentRecentMatches {
    allSeries(
        filter: {
            teamIds: { in: ["opponent-team-id"] }
            startTimeScheduled: {
                gte: "2024-01-01T00:00:00Z"  # Last 30 days
            }
        }
        orderBy: StartTimeScheduled
        orderDirection: DESC
        first: 20
    ) {
        edges {
            node {
                id
                startTimeScheduled
                teams {
                    baseInfo { name }
                }
            }
        }
    }
}
```

#### Strategy Patterns

**From Series State API:**
- **Draft Patterns:**
  - `draftActions` - Complete pick/ban sequences
  - Champion preferences per player
  - First pick priorities
  - Ban patterns

- **Map Preferences:**
  - `map.name` - Maps played
  - Win rates per map
  - Map-specific strategies

- **Team Compositions:**
  - Champion combinations used
  - Role assignments
  - Composition win rates

- **Playstyle Indicators:**
  - `forwardPercentage` - Aggression level
  - `visionScore` - Vision control style
  - `damagePerMinute` - Tempo preferences
  - `baronPowerPlays` - Objective focus

#### Player Tendencies

**From Series State API:**
- Champion pools per player
- Performance on different champions
- Role preferences
- Individual playstyle metrics

**From File Download API:**
- Event data showing:
  - Default setups (for VAL)
  - Rotation patterns
  - Objective timing
  - Aggression windows

### 🔍 Use Cases for Category 2

1. **Common Strategies:**
   - "Team X prefers early game compositions (70% of games)"
   - "Team X prioritizes vision control (avg vision score: 120)"
   - "Team X's default setup on Map Y is..."

2. **Player Tendencies:**
   - "Player A prefers champions: [list] with 65% win rate"
   - "Player B has highest damage on [champion]"
   - "Player C tends to play aggressively (high forward %)"

3. **Draft Patterns:**
   - "Team X typically bans: [champions]"
   - "Team X first picks: [champions] 80% of time"
   - "Team X's favorite composition: [champions]"

4. **Weaknesses:**
   - "Team X struggles on Map Y (30% win rate)"
   - "Team X has low vision score in late game"
   - "Player A has high death rate when playing [champion]"

### 📊 Data Queries Needed

```graphql
# 1. Get opponent's recent series
query OpponentSeries {
    allSeries(
        filter: {
            teamIds: { in: ["opponent-id"] }
            startTimeScheduled: { gte: "date-30-days-ago" }
        }
    ) {
        edges {
            node { id startTimeScheduled }
        }
    }
}

# 2. For each series, get draft and performance
query OpponentSeriesDetails {
    seriesState(id: "series-id") {
        games {
            draftActions {
                type  # PICK or BAN
                sequenceNumber
                draftable { name }
            }
            map { name }
            teams {
                won
                players {
                    character { name }
                }
            }
        }
    }
}

# 3. Aggregate patterns
# Process multiple series to find:
# - Most played champions
# - Most banned champions
# - Win rates per map
# - Composition preferences
```

---

## Category 3: AI Drafting Assistant / Draft Predictor

**Goal:** Recommend optimal draft strategies based on historical data, champion pools, and opponent analysis.

### ✅ Available Data

#### Draft History

**From Series State API:**
- **Complete Draft Sequences:**
  ```graphql
  draftActions {
      id
      type          # PICK or BAN
      sequenceNumber
      drafter {
          id
          type      # TEAM or PLAYER
      }
      draftable {
          id
          type      # CHARACTER, etc.
          name      # Champion name
      }
  }
  ```

- Draft order information
- Which team picked/banned what
- Draft timing data

#### Champion Performance Data

**From Series State API:**
- **Champion Win Rates:**
  - Query multiple series with same champion
  - Calculate win/loss per champion
  - Per player champion performance

- **Champion Statistics:**
  - Average KDA per champion
  - Average damage per champion
  - Champion performance in different roles

- **Champion Synergies:**
  - Compositions that win together
  - Champion combinations with high win rates
  - Team composition effectiveness

#### Player Champion Pools

**From Series State API:**
- Historical champion selections per player
- Player performance on each champion
- Champion preferences by role

**From Central Data API:**
- Player roles (MID, TOP, JUNGLE, etc.)
- Team rosters
- Player-team associations

#### Content Catalog

**From Central Data API:**
- **All Available Champions:**
  ```graphql
  contentCatalogEntities(
      filter: { entityType: { in: [CHARACTER] } }
  ) {
      edges {
          node {
              id
              name
              imageUrl
          }
      }
  }
  ```

- Champion metadata
- Patch/version information

#### Opponent Analysis

**From Series State API:**
- Opponent's draft history
- Opponent's champion preferences
- Opponent's ban patterns
- Opponent's composition preferences

### 🔍 Use Cases for Category 3

1. **Draft Recommendations:**
   - "Based on opponent's history, recommend banning: [champions]"
   - "Player X has 80% win rate on [champion], consider picking"
   - "Composition [champions] has 70% win rate against opponent's style"

2. **Real-Time Draft Assistance:**
   - "Opponent banned [champion], they likely want [champion]"
   - "Your team needs [role], available strong picks: [list]"
   - "Counter-pick to [opponent champion]: [recommendations]"

3. **Synergy Analysis:**
   - "Champions [A, B, C] have 75% win rate together"
   - "Avoid picking [champion] with [champion] (30% win rate)"
   - "Recommended composition based on current picks: [champions]"

4. **Predictive Drafting:**
   - Predict opponent's next pick based on patterns
   - Identify opponent's likely strategy
   - Recommend counter-strategies

### 📊 Data Queries Needed

```graphql
# 1. Get draft history for analysis
query DraftHistory {
    allSeries(
        filter: {
            teamIds: { in: ["team-id", "opponent-id"] }
        }
    ) {
        edges {
            node { id }
        }
    }
}

# For each series:
query DraftDetails {
    seriesState(id: "series-id") {
        games {
            draftActions {
                type
                sequenceNumber
                drafter { type id }
                draftable { name type }
            }
            teams {
                won
                players {
                    character { name }
                }
            }
        }
    }
}

# 2. Get champion performance data
# Aggregate across multiple series:
# - Win rate per champion
# - Win rate per champion combination
# - Player-champion performance
# - Champion performance vs specific opponents

# 3. Get opponent draft patterns
query OpponentDrafts {
    # Get opponent's recent series
    # Extract draft actions
    # Identify patterns:
    #   - Preferred first picks
    #   - Common bans
    #   - Composition preferences
}
```

### 🎯 Implementation Strategy for Category 3

1. **Data Collection Phase:**
   - Query all recent series for both teams
   - Extract all draft actions
   - Extract all game outcomes
   - Build champion performance database

2. **Pattern Recognition:**
   - Identify champion synergies (which champs win together)
   - Identify champion counters (which champs beat others)
   - Identify team draft patterns
   - Identify player champion pools

3. **Real-Time Recommendations:**
   - During draft, analyze current state
   - Consider opponent's likely picks
   - Recommend optimal next move
   - Consider team composition needs

---

## Data Availability Summary

### ✅ Fully Available

| Data Type | Category 1 | Category 2 | Category 3 |
|-----------|------------|-----------|------------|
| Player KDA | ✅ | ✅ | ✅ |
| Damage Stats | ✅ | ✅ | ✅ |
| Vision Score | ✅ | ✅ | ✅ |
| Gold/Economy | ✅ | ✅ | ✅ |
| Champion Data | ✅ | ✅ | ✅ |
| Draft Actions | ✅ | ✅ | ✅ |
| Team Compositions | ✅ | ✅ | ✅ |
| Map Performance | ✅ | ✅ | ✅ |
| Historical Series | ✅ | ✅ | ✅ |
| Event-by-Event Data | ✅ | ✅ | ⚠️ (via File Download) |

### ⚠️ Requires Aggregation

- **Champion Win Rates:** Need to query multiple series and calculate
- **Champion Synergies:** Need to analyze compositions across many games
- **Player Patterns:** Need historical data aggregation
- **Opponent Patterns:** Need to query and process multiple opponent series

### ❌ Not Directly Available (May Need External Data)

- **Patch Information:** Content catalog versions exist but patch notes/changes not in API
- **Meta Analysis:** Need to aggregate data to determine current meta
- **Champion Counters:** Need to calculate from win/loss data
- **Real-Time Draft State:** Need to track draft as it happens (API provides historical)

---

## Recommended Data Collection Strategy

### For All Categories:

1. **Build Historical Database:**
   ```python
   # Query all series for past 2 years (hackathon limit)
   # Store: series_id, teams, players, outcomes, draft actions
   ```

2. **Process Series State Data:**
   ```python
   # For each series:
   # - Extract player stats
   # - Extract team stats
   # - Extract draft actions
   # - Extract game outcomes
   ```

3. **Process Event Data (Category 1 & 2):**
   ```python
   # Download and parse JSONL files
   # Extract: kills, deaths, objectives, timestamps
   # Build event timeline
   ```

4. **Build Aggregation Tables:**
   ```python
   # Champion win rates
   # Player-champion performance
   # Team composition effectiveness
   # Opponent patterns
   ```

---

## Next Steps

1. **Run `data_explorer.py`** to see actual data structure:
   ```bash
   python3 data_explorer.py [api-key] [series-id]
   ```

2. **Run `query_available_data.py`** to test what's actually available:
   ```bash
   python3 query_available_data.py [api-key] [series-id]
   ```

3. **Choose a Category** and build data collection pipeline

4. **Build Aggregation Layer** to process historical data

5. **Create Analysis Engine** for your chosen category

6. **Build UI/Interface** to present insights

---

## Example Queries for Each Category

See:
- `CENTRAL_DATA_API_REFERENCE.md` - Complete Central Data API reference
- `SERIES_STATE_API_DOCS.md` - Series State API documentation
- `FILE_DOWNLOAD_API_DOCS.md` - File Download API documentation
- `CATEGORY_DATA_MAPPING.md` - Detailed mapping with code examples

---

## Confirmed Working Queries

Based on actual API testing:

✅ **Series State API** - Basic queries work, returns:
- Team and player stats
- Game outcomes
- Champion selections
- Draft actions (in games)

✅ **Central Data API** - Returns:
- 18,594+ players
- Teams, series, tournaments
- Content catalog

✅ **File Download API** - Returns:
- Events file (JSONL) - ready for download
- End state file (JSON) - ready for download

