#!/usr/bin/env python3
"""
Comprehensive Data Explorer
Queries all three APIs to see what data is available for hackathon categories.
"""

import json
import urllib.request
import urllib.parse
import ssl
from typing import Dict, Any, Optional
import os
import sys

# Import shared functions
sys.path.insert(0, os.path.dirname(__file__))
from api_explorer import query_graphql as query_central_data, API_URL
from series_state_api import query_graphql as query_series_state, SERIES_STATE_API_URL
from file_download_api import list_files, FILE_DOWNLOAD_BASE_URL
from utils import get_api_key

def explore_central_data(api_key: str, series_id: str = "2616372"):
    """Explore Central Data API for detailed information."""
    print("=" * 80)
    print("📊 CENTRAL DATA API EXPLORATION")
    print("=" * 80)
    print()
    
    results = {}
    
    # 1. Get detailed series information
    print("1️⃣  Getting detailed Series information...")
    query = """
    query DetailedSeries {
        series(id: "%s") {
            id
            startTimeScheduled
            format {
                id
                name
                nameShortened
            }
            type
            title {
                id
                name
                nameShortened
            }
            tournament {
                id
                name
                nameShortened
                startDate
                endDate
            }
            teams {
                baseInfo {
                    id
                    name
                    nameShortened
                    logoUrl
                    colorPrimary
                    colorSecondary
                    rating
                }
                scoreAdvantage
            }
            players {
                id
                nickname
                fullName
                age
                nationality {
                    code
                    name
                }
                team {
                    id
                    name
                }
                roles {
                    id
                    name
                }
                externalLinks {
                    dataProvider {
                        name
                    }
                    externalEntity {
                        id
                    }
                }
            }
        }
    }
    """ % series_id
    
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result and result["data"].get("series"):
            series = result["data"]["series"]
            results["series"] = series
            print(f"   ✅ Series: {series.get('title', {}).get('name')} - {series.get('tournament', {}).get('name')}")
            print(f"   Teams: {len(series.get('teams', []))}")
            print(f"   Players: {len(series.get('players', []))}")
        else:
            print("   ❌ No series data")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 2. Get player details
    print("2️⃣  Getting Player information...")
    query = """
    query Players {
        players(
            filter: { titleId: "3" }
            first: 5
        ) {
            edges {
                node {
                    id
                    nickname
                    fullName
                    age
                    nationality {
                        code
                        name
                    }
                    team {
                        id
                        name
                    }
                    roles {
                        id
                        name
                    }
                    title {
                        id
                        name
                    }
                }
            }
            totalCount
        }
    }
    """
    
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result and result["data"].get("players"):
            players = result["data"]["players"]
            results["players"] = players
            print(f"   ✅ Found {players.get('totalCount', 0)} players")
            print(f"   Sample players:")
            for edge in players.get("edges", [])[:3]:
                player = edge["node"]
                print(f"      - {player.get('nickname')} ({player.get('team', {}).get('name', 'No team')})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 3. Get team details
    print("3️⃣  Getting Team information...")
    query = """
    query Teams {
        teams(
            filter: { titleId: "3" }
            first: 5
        ) {
            edges {
                node {
                    id
                    name
                    nameShortened
                    logoUrl
                    colorPrimary
                    colorSecondary
                    rating
                    title {
                        id
                        name
                    }
                    organization {
                        id
                        name
                    }
                }
            }
            totalCount
        }
    }
    """
    
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result and result["data"].get("teams"):
            teams = result["data"]["teams"]
            results["teams"] = teams
            print(f"   ✅ Found {teams.get('totalCount', 0)} teams")
            print(f"   Sample teams:")
            for edge in teams.get("edges", [])[:3]:
                team = edge["node"]
                print(f"      - {team.get('name')} (Rating: {team.get('rating', 'N/A')})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 4. Get content catalog (champions/items/maps)
    print("4️⃣  Getting Content Catalog (Champions/Items/Maps)...")
    query = """
    query ContentCatalog {
        contentCatalogVersions(
            filter: { title: { id: { in: ["3"] } } }
            first: 1
        ) {
            edges {
                node {
                    id
                    name
                    publishedOn
                    title {
                        name
                    }
                }
            }
        }
    }
    """
    
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result and result["data"].get("contentCatalogVersions"):
            versions = result["data"]["contentCatalogVersions"]
            if versions.get("edges"):
                version = versions["edges"][0]["node"]
                results["content_catalog_version"] = version
                print(f"   ✅ Latest version: {version.get('name')} (Published: {version.get('publishedOn')})")
                
                # Get characters (champions)
                char_query = """
                query Characters {
                    contentCatalogEntities(
                        contentCatalogVersionId: "%s"
                        filter: { entityType: { in: [CHARACTER] } }
                        first: 10
                    ) {
                        edges {
                            node {
                                id
                                name
                                imageUrl
                            }
                        }
                        totalCount
                    }
                }
                """ % version["id"]
                
                char_result = query_central_data(char_query, api_key=api_key)
                if "data" in char_result and char_result["data"].get("contentCatalogEntities"):
                    chars = char_result["data"]["contentCatalogEntities"]
                    results["characters"] = chars
                    print(f"   ✅ Found {chars.get('totalCount', 0)} champions/characters")
                    print(f"   Sample: {', '.join([e['node']['name'] for e in chars.get('edges', [])[:5]])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    return results

def explore_series_state(api_key: str, series_id: str = "2616372"):
    """Explore Series State API for match statistics."""
    print("=" * 80)
    print("🎮 SERIES STATE API EXPLORATION")
    print("=" * 80)
    print()
    
    results = {}
    
    # Get comprehensive series state
    print("1️⃣  Getting comprehensive Series State...")
    query = """
    query ComprehensiveSeriesState {
        seriesState(id: "%s") {
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
                    damagePerMinute
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
                        character {
                            id
                            name
                        }
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
                draftActions {
                    id
                    type
                    sequenceNumber
                    drafter {
                        id
                        type
                    }
                    draftable {
                        id
                        type
                        name
                    }
                }
            }
        }
    }
    """ % series_id
    
    try:
        result = query_series_state(query, api_key=api_key)
        if "data" in result and result["data"].get("seriesState"):
            state = result["data"]["seriesState"]
            results["series_state"] = state
            print(f"   ✅ Series State retrieved")
            print(f"   Title: {state.get('title', {}).get('nameShortened')}")
            print(f"   Format: {state.get('format')}")
            print(f"   Status: {'Finished' if state.get('finished') else 'In Progress'}")
            print(f"   Games: {len(state.get('games', []))}")
            
            # Check for draft actions
            draft_actions = []
            for game in state.get("games", []):
                draft_actions.extend(game.get("draftActions", []))
            if draft_actions:
                results["draft_actions"] = draft_actions
                print(f"   ✅ Found {len(draft_actions)} draft actions (picks/bans)")
            
            # Check for player stats
            all_players = []
            for team in state.get("teams", []):
                all_players.extend(team.get("players", []))
            if all_players:
                print(f"   ✅ Player stats available for {len(all_players)} players")
                print(f"   Sample stats: KDA, Damage, Vision Score, Gold, etc.")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    return results

def explore_file_download(api_key: str, series_id: str = "2616372"):
    """Explore File Download API."""
    print("=" * 80)
    print("📥 FILE DOWNLOAD API EXPLORATION")
    print("=" * 80)
    print()
    
    results = {}
    
    print("1️⃣  Checking available files...")
    try:
        file_list = list_files(series_id, api_key)
        files = file_list.get("files", [])
        results["files"] = files
        
        print(f"   ✅ Found {len(files)} file types")
        for file_info in files:
            file_id = file_info.get("id")
            status = file_info.get("status")
            desc = file_info.get("description")
            print(f"      - {file_id}: {desc} (Status: {status})")
            
            if file_id == "events-grid" and status == "ready":
                results["events_available"] = True
                print(f"        → Event-by-event data available (JSONL)")
            elif file_id == "state-grid" and status == "ready":
                results["end_state_available"] = True
                print(f"        → End state data available (JSON)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    return results

def analyze_for_categories(central_data: Dict, series_state: Dict, file_download: Dict):
    """Analyze available data for each hackathon category."""
    print("=" * 80)
    print("🎯 DATA ANALYSIS FOR HACKATHON CATEGORIES")
    print("=" * 80)
    print()
    
    analysis = {
        "category1": {"available": [], "missing": []},
        "category2": {"available": [], "missing": []},
        "category3": {"available": [], "missing": []}
    }
    
    # Category 1: Assistant Coach (Micro + Macro Analytics)
    print("📊 Category 1: Assistant Coach (Micro + Macro Analytics)")
    print("-" * 80)
    
    # Micro-level (player analytics)
    if series_state.get("series_state"):
        state = series_state["series_state"]
        players = []
        for team in state.get("teams", []):
            players.extend(team.get("players", []))
        
        if players:
            analysis["category1"]["available"].extend([
                "✅ Player KDA (kills, deaths, assists)",
                "✅ Damage dealt/taken (total, percentage, per minute)",
                "✅ Vision score (total, per minute)",
                "✅ Gold earned (total, per minute)",
                "✅ Kill participation",
                "✅ Forward percentage (time on enemy side)",
                "✅ Character/champion played",
                "✅ Game-by-game performance breakdown"
            ])
    
    # Macro-level (team strategy)
    if series_state.get("series_state"):
        state = series_state["series_state"]
        teams = state.get("teams", [])
        if teams:
            analysis["category1"]["available"].extend([
                "✅ Team damage dealt/taken",
                "✅ Team vision score",
                "✅ Team KDA ratio",
                "✅ Baron power plays",
                "✅ Game outcomes (wins/losses)",
                "✅ Map performance"
            ])
    
    # Historical data
    if file_download.get("events_available"):
        analysis["category1"]["available"].append("✅ Event-by-event historical data (every kill, death, objective)")
    
    if central_data.get("series"):
        analysis["category1"]["available"].extend([
            "✅ Series metadata (format, tournament, date)",
            "✅ Player team affiliations",
            "✅ Player roles/positions"
        ])
    
    print("Available Data:")
    for item in analysis["category1"]["available"]:
        print(f"  {item}")
    
    print()
    
    # Category 2: Automated Scouting Report Generator
    print("🔍 Category 2: Automated Scouting Report Generator")
    print("-" * 80)
    
    if central_data.get("series"):
        analysis["category2"]["available"].extend([
            "✅ Recent match history (via allSeries query)",
            "✅ Opponent team information",
            "✅ Opponent player rosters",
            "✅ Match dates and tournaments"
        ])
    
    if series_state.get("series_state"):
        state = series_state["series_state"]
        if state.get("games"):
            analysis["category2"]["available"].extend([
                "✅ Map preferences",
                "✅ Draft actions (picks/bans)",
                "✅ Champion/character selections",
                "✅ Team compositions",
                "✅ Win/loss patterns"
            ])
    
    if series_state.get("draft_actions"):
        analysis["category2"]["available"].append("✅ Detailed draft history (pick/ban sequences)")
    
    if file_download.get("events_available"):
        analysis["category2"]["available"].append("✅ Detailed event data for strategy analysis")
    
    print("Available Data:")
    for item in analysis["category2"]["available"]:
        print(f"  {item}")
    
    print()
    
    # Category 3: AI Drafting Assistant
    print("🤖 Category 3: AI Drafting Assistant / Draft Predictor")
    print("-" * 80)
    
    if series_state.get("draft_actions"):
        analysis["category3"]["available"].extend([
            "✅ Draft action sequences (picks/bans)",
            "✅ Draft order information",
            "✅ Champion/character selections",
            "✅ Draft outcomes (win/loss)"
        ])
    
    if series_state.get("series_state"):
        state = series_state["series_state"]
        players = []
        for team in state.get("teams", []):
            players.extend(team.get("players", []))
        
        if players:
            analysis["category3"]["available"].extend([
                "✅ Player champion pools (from historical games)",
                "✅ Champion performance (win rates, KDA, damage)",
                "✅ Player-champion combinations"
            ])
    
    if central_data.get("characters"):
        analysis["category3"]["available"].append("✅ Champion/character catalog (all available champions)")
    
    if central_data.get("series"):
        analysis["category3"]["available"].extend([
            "✅ Team composition history",
            "✅ Matchup data (team vs team)",
            "✅ Tournament context"
        ])
    
    # Check for patch/version data
    if central_data.get("content_catalog_version"):
        analysis["category3"]["available"].append("✅ Content catalog versions (patch data)")
    
    print("Available Data:")
    for item in analysis["category3"]["available"]:
        print(f"  {item}")
    
    print()
    
    return analysis

def main():
    # Get API key (prioritizes .env file, then env var, then command line)
    api_key = get_api_key()
    
    # Use a known Series ID (T1 vs Gen.G from earlier)
    series_id = "2616372" if len(sys.argv) < 3 else sys.argv[2]
    
    print(f"🔍 Exploring data for Series ID: {series_id}")
    print()
    
    # Explore all APIs
    central_data = explore_central_data(api_key, series_id)
    series_state = explore_series_state(api_key, series_id)
    file_download = explore_file_download(api_key, series_id)
    
    # Analyze for categories
    analysis = analyze_for_categories(central_data, series_state, file_download)
    
    # Save results
    output = {
        "series_id": series_id,
        "central_data": central_data,
        "series_state": series_state,
        "file_download": file_download,
        "category_analysis": analysis
    }
    
    filename = f"data_exploration_{series_id}.json"
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("=" * 80)
    print(f"💾 Full exploration data saved to: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    main()

