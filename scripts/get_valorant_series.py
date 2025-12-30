#!/usr/bin/env python3
"""
Get a random Valorant Americas series ID
"""

import json
import sys
import os
import random
sys.path.insert(0, os.path.dirname(__file__))
from api_explorer import query_graphql, API_URL, get_headers
from utils import get_api_key
import urllib.request
import ssl

def main():
    # Get API key (prioritizes .env file, then env var, then command line)
    api_key = get_api_key()
    
    print("🔍 Finding Valorant Americas series...")
    print()
    
    # 1. Find Valorant title ID
    print("1. Getting Valorant title ID...")
    query = """
    query Titles {
        titles {
            id
            name
        }
    }
    """
    
    result = query_graphql(query, api_key=api_key)
    if "data" in result:
        titles = result["data"].get("titles", [])
        valorant_title = next((t for t in titles if "valorant" in t.get("name", "").lower()), None)
        if not valorant_title:
            print("❌ Valorant title not found")
            return
        valorant_id = valorant_title["id"]
        print(f"   ✅ Valorant title ID: {valorant_id}")
    else:
        print("❌ Could not get titles")
        return
    
    print()
    
    # 2. Find Americas tournaments
    print("2. Finding Valorant Americas tournaments...")
    query = """
    query Tournaments {
        tournaments(
            filter: { 
                title: { id: { in: ["%s"] } }
                name: { contains: "Americas" }
            }
            first: 20
        ) {
            edges {
                node {
                    id
                    name
                }
            }
            totalCount
        }
    }
    """ % valorant_id
    
    result = query_graphql(query, api_key=api_key)
    if "data" in result:
        tournaments = result["data"].get("tournaments", {})
        tournament_edges = tournaments.get("edges", [])
        print(f"   ✅ Found {tournaments.get('totalCount', 0)} tournaments")
        
        if not tournament_edges:
            print("   ⚠️  No tournaments found, trying without 'Americas' filter...")
            # Try without Americas filter
            query2 = """
            query Tournaments {
                tournaments(
                    filter: { title: { id: { in: ["%s"] } } }
                    first: 50
                ) {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
            """ % valorant_id
            result2 = query_graphql(query2, api_key=api_key)
            if "data" in result2:
                tournament_edges = result2["data"].get("tournaments", {}).get("edges", [])
                # Filter for Americas manually
                tournament_edges = [t for t in tournament_edges if "americas" in t["node"]["name"].lower()]
        
        if not tournament_edges:
            print("   ❌ No Americas tournaments found")
            return
        
        # Pick a random tournament
        tournament = random.choice(tournament_edges)["node"]
        tournament_id = tournament["id"]
        print(f"   ✅ Selected tournament: {tournament['name']} (ID: {tournament_id})")
    else:
        print("❌ Could not get tournaments")
        return
    
    print()
    
    # 3. Get series from tournament
    print("3. Getting series from tournament...")
    query = """
    query AllSeries {
        allSeries(
            filter: { 
                tournament: { 
                    id: { in: [%s] }, 
                    includeChildren: { equals: true } 
                } 
            }
            orderBy: StartTimeScheduled
            first: 50
        ) {
            edges {
                node {
                    id
                    startTimeScheduled
                    teams {
                        baseInfo {
                            name
                        }
                    }
                }
            }
            totalCount
        }
    }
    """ % tournament_id
    
    result = query_graphql(query, api_key=api_key)
    if "data" in result:
        all_series = result["data"].get("allSeries", {})
        series_edges = all_series.get("edges", [])
        total_count = all_series.get("totalCount", 0)
        
        print(f"   ✅ Found {total_count} series")
        
        if not series_edges:
            print("   ❌ No series found in this tournament")
            return
        
        # Pick a random series
        series = random.choice(series_edges)["node"]
        series_id = series["id"]
        teams = [t["baseInfo"]["name"] for t in series.get("teams", [])]
        
        print()
        print("=" * 80)
        print("🎯 RANDOM VALORANT AMERICAS SERIES")
        print("=" * 80)
        print(f"Series ID: {series_id}")
        print(f"Teams: {' vs '.join(teams) if teams else 'TBD'}")
        print(f"Scheduled: {series.get('startTimeScheduled', 'N/A')}")
        print("=" * 80)
        print()
        print(f"Use this Series ID: {series_id}")
        print()
        print("Test it with:")
        print(f"  python3 series_state_api.py [api-key] {series_id}")
        print(f"  python3 file_download_api.py [api-key] {series_id}")
    else:
        print("❌ Could not get series")

if __name__ == "__main__":
    main()

