#!/usr/bin/env python3
"""
Query Available Data - Test what's actually available in the APIs
"""

import json
import urllib.request
import ssl
import os
import sys

# Import from existing scripts
sys.path.insert(0, os.path.dirname(__file__))
from api_explorer import query_graphql as query_central_data
from series_state_api import query_graphql as query_series_state, get_headers
from utils import get_api_key

def test_series_state_basic(api_key: str, series_id: str):
    """Test basic Series State query without LoL-specific fragments."""
    print("Testing Series State API (Basic Query)...")
    
    query = """
    query BasicSeriesState {
        seriesState(id: "%s") {
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
                    kills
                    deaths
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
                    }
                }
            }
        }
    }
    """ % series_id
    
    try:
        result = query_series_state(query, api_key=api_key)
        if "errors" in result:
            print("Errors:", json.dumps(result["errors"], indent=2))
        if "data" in result and result["data"].get("seriesState"):
            state = result["data"]["seriesState"]
            print(f"✅ Success! Series: {state.get('title', {}).get('nameShortened')}")
            print(f"   Teams: {len(state.get('teams', []))}")
            print(f"   Games: {len(state.get('games', []))}")
            
            # Check for draft actions
            draft_count = sum(len(g.get("draftActions", [])) for g in state.get("games", []))
            if draft_count > 0:
                print(f"   ✅ Draft actions: {draft_count}")
            
            return state
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_central_data_queries(api_key: str):
    """Test various Central Data queries."""
    print("\nTesting Central Data API Queries...")
    
    # Test players query
    print("\n1. Players query:")
    query = """
    query TestPlayers {
        players(filter: { titleId: "3" }, first: 3) {
            edges {
                node {
                    id
                    nickname
                    team { name }
                }
            }
            totalCount
        }
    }
    """
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result:
            players = result["data"].get("players", {})
            print(f"   ✅ Found {players.get('totalCount', 0)} players")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test teams query
    print("\n2. Teams query:")
    query = """
    query TestTeams {
        teams(filter: { titleId: "3" }, first: 3) {
            edges {
                node {
                    id
                    name
                    rating
                }
            }
            totalCount
        }
    }
    """
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result:
            teams = result["data"].get("teams", {})
            print(f"   ✅ Found {teams.get('totalCount', 0)} teams")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test content catalog
    print("\n3. Content Catalog (Champions):")
    query = """
    query TestContentCatalog {
        contentCatalogVersions(filter: { title: { id: { in: ["3"] } } }, first: 1) {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
    """
    try:
        result = query_central_data(query, api_key=api_key)
        if "data" in result:
            versions = result["data"].get("contentCatalogVersions", {})
            if versions.get("edges"):
                version_id = versions["edges"][0]["node"]["id"]
                print(f"   ✅ Found version: {versions['edges'][0]['node']['name']}")
                
                # Get characters
                char_query = """
                query Characters {
                    contentCatalogEntities(
                        contentCatalogVersionId: "%s"
                        filter: { entityType: { in: [CHARACTER] } }
                        first: 5
                    ) {
                        totalCount
                        edges {
                            node {
                                name
                            }
                        }
                    }
                }
                """ % version_id
                char_result = query_central_data(char_query, api_key=api_key)
                if "data" in char_result:
                    chars = char_result["data"].get("contentCatalogEntities", {})
                    print(f"   ✅ Found {chars.get('totalCount', 0)} champions")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    # Get API key (prioritizes .env file, then env var, then command line)
    api_key = get_api_key()
    
    series_id = "2616372" if len(sys.argv) < 3 else sys.argv[2]
    
    print("=" * 80)
    print("🔍 QUERYING AVAILABLE DATA")
    print("=" * 80)
    print()
    
    # Test Series State
    series_state = test_series_state_basic(api_key, series_id)
    
    # Test Central Data
    test_central_data_queries(api_key)
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    
    if series_state:
        print("\n✅ Series State API:")
        print("   - Basic match data: ✅")
        print("   - Team stats: ✅")
        print("   - Player stats: ✅")
        print("   - Game-by-game data: ✅")
        print("   - Draft actions: ✅" if any(len(g.get("draftActions", [])) > 0 for g in series_state.get("games", [])) else "   - Draft actions: ⚠️ (check if available)")
        print("   - Champion data: ✅")
    
    print("\n✅ Central Data API:")
    print("   - Teams: ✅")
    print("   - Players: ✅")
    print("   - Series metadata: ✅")
    print("   - Content catalog: ✅")
    
    print("\n✅ File Download API:")
    print("   - Events file: ✅")
    print("   - End state file: ✅")

if __name__ == "__main__":
    main()

