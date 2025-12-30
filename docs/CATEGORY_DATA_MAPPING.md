# Hackathon Categories - Available Data Mapping

Based on actual API queries, here's what data is available for each category.

## ✅ Confirmed Available Data

### All Categories - Base Data

**From Central Data API:**
- ✅ 18,594+ players in database
- ✅ Teams information
- ✅ Series metadata (dates, tournaments, formats)
- ✅ Content catalog (champions, items, maps)
- ✅ Player roles and positions
- ✅ Team rosters

**From Series State API:**
- ✅ Match outcomes (wins/losses)
- ✅ Team scores
- ✅ Player KDA (kills, deaths, assists)
- ✅ Champion/character selections
- ✅ Game-by-game breakdown
- ✅ Map information

**From File Download API:**
- ✅ Event-by-event data (JSONL) - Every kill, death, objective
- ✅ End state files (JSON) - Final match state

---

## Category 1: Assistant Coach (Micro + Macro Analytics)

### ✅ Confirmed Available

#### Micro-Level Player Data:
- **KDA Metrics:** `kills`, `deaths`, `killAssistsGiven`
- **Champion Data:** `character { name }` - What champion each player played
- **Game Performance:** Per-game stats available
- **Series Performance:** Aggregated stats across series

#### Macro-Level Team Data:
- **Team Scores:** `score`, `won`
- **Team KDA:** `kills`, `deaths` at team level
- **Game Outcomes:** Win/loss per game and series
- **Map Performance:** Which maps played, outcomes

#### Event-Level Data (File Download):
- **Every Event:** Kill, death, assist, objective events
- **Timestamps:** Exact timing of all events
- **Position Data:** Player positions over time (if in events)

### 🔍 How to Use for Category 1:

1. **Query Multiple Series:**
   ```graphql
   # Get all series for a player/team
   allSeries(filter: { teamIds: { in: ["team-id"] } })
   ```

2. **Get Player Stats for Each Series:**
   ```graphql
   # For each series ID
   seriesState(id: "series-id") {
       teams {
           players {
               kills
               deaths
               killAssistsGiven
               character { name }
           }
       }
   }
   ```

3. **Download Event Files:**
   ```python
   # Download events JSONL for detailed analysis
   # Parse every kill, death, objective
   # Build timeline of mistakes
   ```

4. **Identify Patterns:**
   - Aggregate stats across multiple games
   - Find recurring mistakes (high deaths, low vision, etc.)
   - Correlate with team outcomes

### 📊 Example Analysis:

```python
# Pseudo-code for Category 1
for series in player_series_history:
    state = get_series_state(series.id)
    for game in state.games:
        for player in game.players:
            if player.deaths > threshold:
                mistake = {
                    "type": "high_deaths",
                    "game": game.id,
                    "champion": player.character.name,
                    "impact": calculate_team_impact(game)
                }
                mistakes.append(mistake)

# Aggregate mistakes
# Connect to macro outcomes
# Generate insights
```

---

## Category 2: Automated Scouting Report Generator

### ✅ Confirmed Available

#### Opponent Team Data:
- **Team Information:** Name, logo, rating (from Central Data)
- **Recent Series:** Can query all series for a team
- **Match History:** Dates, opponents, outcomes

#### Strategy Patterns:
- **Champion Selections:** What champions opponent plays
- **Map Preferences:** Which maps they play
- **Game Outcomes:** Win/loss patterns
- **Draft Actions:** Pick/ban sequences (if available in games)

#### Player Tendencies:
- **Champion Pools:** What champions each player plays
- **Performance:** KDA, damage on different champions
- **Role Assignments:** Which roles players play

### 🔍 How to Use for Category 2:

1. **Get Opponent's Recent Series:**
   ```graphql
   query OpponentHistory {
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

2. **Analyze Each Series:**
   ```graphql
   # For each series ID
   query SeriesAnalysis {
       seriesState(id: "series-id") {
           games {
               map { name }
               draftActions {
                   type  # PICK or BAN
                   draftable { name }
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
   ```

3. **Build Patterns:**
   - Most played champions
   - Most banned champions
   - Map win rates
   - Composition preferences
   - Draft patterns

### 📊 Example Scouting Report:

```python
# Pseudo-code for Category 2
opponent_series = get_recent_series(opponent_team_id, last_30_days)

champions_played = {}
champions_banned = {}
maps_played = {}
compositions = []

for series in opponent_series:
    state = get_series_state(series.id)
    for game in state.games:
        # Track champions
        for player in game.players:
            champ = player.character.name
            champions_played[champ] = champions_played.get(champ, 0) + 1
        
        # Track bans
        for action in game.draftActions:
            if action.type == "BAN":
                champ = action.draftable.name
                champions_banned[champ] = champions_banned.get(champ, 0) + 1
        
        # Track maps
        map_name = game.map.name
        maps_played[map_name] = maps_played.get(map_name, {"wins": 0, "losses": 0})
        if game.teams[0].won:  # Assuming opponent is team 0
            maps_played[map_name]["wins"] += 1
        else:
            maps_played[map_name]["losses"] += 1

# Generate report
report = {
    "top_champions": sorted(champions_played.items(), key=lambda x: x[1], reverse=True)[:5],
    "common_bans": sorted(champions_banned.items(), key=lambda x: x[1], reverse=True)[:5],
    "map_performance": maps_played,
    "preferred_compositions": analyze_compositions(compositions)
}
```

---

## Category 3: AI Drafting Assistant

### ✅ Confirmed Available

#### Draft Data:
- **Draft Actions:** Available in `games { draftActions }`
  - `type`: PICK or BAN
  - `sequenceNumber`: Draft order
  - `drafter`: Which team/player
  - `draftable`: Champion/character being picked/banned

#### Champion Data:
- **Champion Catalog:** All available champions from content catalog
- **Champion Selections:** What champions were played in each game
- **Player-Champion History:** Can track which champions each player has played

#### Performance Data:
- **Win/Loss:** Can correlate champion picks with outcomes
- **Team Compositions:** Can see which champion combinations win

### ⚠️ Requires Aggregation:

- **Champion Win Rates:** Need to query many series and calculate
- **Champion Synergies:** Need to analyze which champs win together
- **Counter Picks:** Need to analyze matchups
- **Meta Analysis:** Need to aggregate recent data

### 🔍 How to Use for Category 3:

1. **Build Champion Performance Database:**
   ```python
   # Query all recent series
   all_series = get_all_series(last_2_years)  # Hackathon limit
   
   champion_stats = {}
   for series in all_series:
       state = get_series_state(series.id)
       for game in state.games:
           for team in game.teams:
               composition = [p.character.name for p in team.players]
               won = team.won
               
               # Track composition win rate
               comp_key = tuple(sorted(composition))
               if comp_key not in champion_stats:
                   champion_stats[comp_key] = {"wins": 0, "losses": 0}
               
               if won:
                   champion_stats[comp_key]["wins"] += 1
               else:
                   champion_stats[comp_key]["losses"] += 1
   ```

2. **Build Draft History:**
   ```python
   draft_patterns = {}
   for series in all_series:
       state = get_series_state(series.id)
       for game in state.games:
           draft_sequence = []
           for action in sorted(game.draftActions, key=lambda x: x.sequenceNumber):
               draft_sequence.append({
                   "type": action.type,  # PICK or BAN
                   "champion": action.draftable.name,
                   "team": action.drafter.id
               })
           
           # Store draft pattern with outcome
           pattern_key = tuple(draft_sequence)
           draft_patterns[pattern_key] = game.teams[0].won
   ```

3. **Real-Time Draft Assistance:**
   ```python
   # During live draft
   current_draft_state = get_current_draft_state()
   
   # Analyze opponent patterns
   opponent_history = get_opponent_draft_history(opponent_team_id)
   likely_next_pick = predict_next_pick(opponent_history, current_draft_state)
   
   # Recommend counter
   recommendations = get_counter_recommendations(
       likely_next_pick,
       available_champions,
       team_champion_pools
   )
   ```

### 📊 Example Draft Recommendation:

```python
# Pseudo-code for Category 3
def get_draft_recommendations(opponent_team_id, current_draft_state):
    # 1. Get opponent's draft history
    opponent_series = get_recent_series(opponent_team_id)
    opponent_drafts = extract_draft_patterns(opponent_series)
    
    # 2. Predict opponent's next move
    predicted_pick = predict_from_patterns(opponent_drafts, current_draft_state)
    
    # 3. Get champion performance data
    champion_win_rates = get_champion_win_rates()
    champion_synergies = get_champion_synergies()
    
    # 4. Get team's champion pools
    team_champion_pools = get_team_champion_pools(my_team_id)
    
    # 5. Generate recommendations
    recommendations = []
    for champ in available_champions:
        if champ in team_champion_pools:
            win_rate = champion_win_rates.get(champ, 0.5)
            synergy_score = calculate_synergy(champ, current_draft_state.my_picks, champion_synergies)
            counter_score = calculate_counter(champ, predicted_pick, champion_win_rates)
            
            recommendations.append({
                "champion": champ,
                "win_rate": win_rate,
                "synergy_score": synergy_score,
                "counter_score": counter_score,
                "total_score": win_rate * 0.4 + synergy_score * 0.3 + counter_score * 0.3
            })
    
    return sorted(recommendations, key=lambda x: x["total_score"], reverse=True)
```

---

## Data Collection Strategy

### Step 1: Build Historical Database

```python
# Query all available series (past 2 years)
series_list = []
cursor = None
while True:
    result = query_all_series(
        filter={...},
        first=100,
        after=cursor
    )
    series_list.extend(result.edges)
    if not result.pageInfo.hasNextPage:
        break
    cursor = result.pageInfo.endCursor

# Store: series_id, teams, date, tournament
```

### Step 2: Collect Series State Data

```python
# For each series
for series in series_list:
    state = get_series_state(series.id)
    
    # Store:
    # - Player stats per game
    # - Team stats per game
    # - Draft actions
    # - Champion selections
    # - Outcomes
```

### Step 3: Process Event Files (Categories 1 & 2)

```python
# Download and parse JSONL
for series in series_list:
    events_file = download_events_file(series.id)
    events = parse_jsonl(events_file)
    
    # Extract:
    # - Every kill/death with timestamp
    # - Objective timings
    # - Position data
    # - Item purchases
```

### Step 4: Build Aggregation Tables

```python
# Champion win rates
champion_win_rates = calculate_win_rates(all_series_data)

# Champion synergies
champion_synergies = find_winning_combinations(all_series_data)

# Player patterns
player_patterns = analyze_player_performance(all_series_data)

# Team patterns
team_patterns = analyze_team_strategies(all_series_data)
```

---

## Quick Reference: What Each Category Needs

### Category 1: Assistant Coach
**Primary Data Sources:**
- Series State API (player/team stats)
- File Download API (event data)
- Central Data API (metadata)

**Key Metrics:**
- Player KDA, damage, vision, gold
- Team aggregates
- Event timeline
- Mistake identification

### Category 2: Scouting Report
**Primary Data Sources:**
- Central Data API (opponent series list)
- Series State API (match analysis)
- File Download API (strategy patterns)

**Key Metrics:**
- Recent match history
- Champion preferences
- Draft patterns
- Map performance
- Composition preferences

### Category 3: Drafting Assistant
**Primary Data Sources:**
- Series State API (draft actions, outcomes)
- Central Data API (champion catalog, player pools)
- Historical aggregation (win rates, synergies)

**Key Metrics:**
- Draft sequences
- Champion win rates
- Champion synergies
- Player champion pools
- Opponent patterns

---

## Next Steps

1. **Choose your category**
2. **Run data collection scripts** to build your database
3. **Process and aggregate** the data
4. **Build your analysis engine**
5. **Create the UI/interface**

See the individual API documentation files for detailed query examples:
- `CENTRAL_DATA_API_REFERENCE.md`
- `SERIES_STATE_API_DOCS.md`
- `FILE_DOWNLOAD_API_DOCS.md`

