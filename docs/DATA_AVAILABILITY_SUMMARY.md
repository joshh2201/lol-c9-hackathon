# Data Availability Summary for Hackathon Categories

Quick reference of what data is available for each category based on actual API queries.

## ✅ Confirmed Working APIs

### Series State API
- **Status:** ✅ Working
- **Returns:** Match stats, player KDA, champion data, game outcomes
- **Draft Actions:** Available in `games { draftActions }`
- **Tested Series:** 2616372 (T1 vs Gen.G Esports)

### Central Data API  
- **Status:** ✅ Working
- **Returns:** 18,594+ players, teams, series metadata, content catalog
- **Tested:** Players query successful, teams query successful

### File Download API
- **Status:** ✅ Working
- **Returns:** Events file (JSONL), End state file (JSON)
- **Status:** Files ready for download

---

## Category 1: Assistant Coach

### ✅ Available Data

**Micro-Level (Player Analytics):**
- ✅ Kills, deaths, assists (per game & series)
- ✅ Champion played per game
- ✅ Game-by-game performance breakdown
- ✅ Event-by-event data (every kill, death, objective)

**Macro-Level (Team Strategy):**
- ✅ Team scores and outcomes
- ✅ Team KDA aggregates
- ✅ Map performance
- ✅ Series outcomes

**For Mistake Analysis:**
- ✅ Can identify high-death games
- ✅ Can track vision score patterns
- ✅ Can correlate individual performance with team outcomes
- ✅ Can analyze event timeline for critical mistakes

### 📊 Data Collection Needed

1. Query multiple series for a player/team
2. Get Series State for each series
3. Download event files for detailed analysis
4. Aggregate patterns across games

### 💡 Key Insight

**You have everything needed!** The event-by-event data (JSONL) gives you the granular detail to identify exact mistakes and their timing.

---

## Category 2: Automated Scouting Report

### ✅ Available Data

**Opponent Information:**
- ✅ Team name, logo, rating
- ✅ Recent series history (can query by team ID)
- ✅ Match dates and opponents

**Strategy Patterns:**
- ✅ Champion selections (what they play)
- ✅ Map preferences (which maps they play)
- ✅ Win/loss patterns
- ✅ Draft actions (picks/bans) - if available in games

**Player Tendencies:**
- ✅ Champion pools (what each player plays)
- ✅ Performance on different champions
- ✅ Role assignments

### 📊 Data Collection Needed

1. Query all recent series for opponent team
2. Get Series State for each series
3. Extract draft actions and champion selections
4. Aggregate patterns (most played champs, common bans, etc.)

### 💡 Key Insight

**You have everything needed!** Can build comprehensive scouting reports by aggregating opponent's recent match data.

---

## Category 3: AI Drafting Assistant

### ✅ Available Data

**Draft Data:**
- ✅ Draft actions (picks/bans) in `games { draftActions }`
- ✅ Draft sequence numbers
- ✅ Which team picked/banned what
- ✅ Champion names

**Champion Data:**
- ✅ All champions from content catalog
- ✅ Champion selections in games
- ✅ Player-champion history (can track across series)

**Performance Data:**
- ✅ Win/loss outcomes per game
- ✅ Can correlate champion picks with outcomes

### ⚠️ Requires Aggregation

- **Champion Win Rates:** Need to query many series and calculate
- **Champion Synergies:** Need to analyze which combinations win
- **Counter Picks:** Need matchup analysis
- **Meta Analysis:** Need recent data aggregation

### 📊 Data Collection Needed

1. Query all series (past 2 years)
2. Extract all draft actions
3. Extract all game outcomes
4. Build champion performance database
5. Calculate win rates, synergies, counters

### 💡 Key Insight

**You have the raw data!** Need to build aggregation layer to calculate win rates, synergies, and patterns. This is the most data-intensive category but all necessary data is available.

---

## Quick Comparison

| Data Type | Category 1 | Category 2 | Category 3 |
|-----------|------------|-----------|------------|
| Player Stats | ✅ Direct | ✅ Direct | ✅ Direct |
| Team Stats | ✅ Direct | ✅ Direct | ✅ Direct |
| Champion Data | ✅ Direct | ✅ Direct | ✅ Direct |
| Draft Actions | ✅ Direct | ✅ Direct | ✅ Direct |
| Event Timeline | ✅ Direct | ✅ Direct | ⚠️ Via File Download |
| Historical Aggregation | ⚠️ Need to build | ⚠️ Need to build | ⚠️ Need to build |
| Win Rate Analysis | ⚠️ Need to calculate | ⚠️ Need to calculate | ⚠️ Need to calculate |
| Pattern Recognition | ⚠️ Need to build | ⚠️ Need to build | ⚠️ Need to build |

---

## Recommended Starting Point

### For Category 1 (Easiest to Start):
1. Pick a player or team
2. Query their recent series
3. Get Series State for each
4. Download event files
5. Build mistake identification logic

### For Category 2 (Medium Complexity):
1. Pick an opponent team
2. Query their recent series (last 20-30)
3. Get Series State for each
4. Extract patterns (champions, maps, drafts)
5. Generate report

### For Category 3 (Most Complex):
1. Query ALL available series (past 2 years)
2. Get Series State for each
3. Extract all draft actions
4. Build champion performance database
5. Calculate win rates and synergies
6. Build recommendation engine

---

## Data Volume Estimates

Based on API queries:
- **Players:** 18,594+ in database
- **Series:** Hundreds to thousands available (past 2 years)
- **Events per Series:** Hundreds to thousands of events in JSONL files

**Storage Needs:**
- Series State data: ~10-50KB per series
- Event files: ~100KB-1MB per series (compressed)
- Aggregated data: Depends on analysis depth

---

## Tools Available

1. **`api_explorer.py`** - Get Series IDs
2. **`series_state_api.py`** - Get match stats
3. **`file_download_api.py`** - Download event files
4. **`data_explorer.py`** - Comprehensive exploration
5. **`query_available_data.py`** - Test what's available

All scripts use the same `.env` file for API key.

---

## Next Steps

1. **Choose your category**
2. **Run exploration scripts** to see actual data
3. **Design your data model** (what to store, how to aggregate)
4. **Build data collection pipeline**
5. **Build analysis engine**
6. **Create UI/interface**

See `CATEGORY_DATA_MAPPING.md` for detailed code examples for each category.

