#!/usr/bin/env python3
"""
Grid.gg Central Data API Explorer
Explores the GraphQL API to understand available data and structure.
"""

import json
import urllib.request
import urllib.parse
import ssl
from typing import Dict, Any, Optional
import os
import sys

# Import shared utilities
sys.path.insert(0, os.path.dirname(__file__))
from utils import get_api_key

# API endpoint
API_URL = "https://api-op.grid.gg/central-data/graphql"

# Headers - add API key if available
def get_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    """Get request headers with optional API key."""
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        # Grid.gg APIs use x-api-key header (not Authorization: Bearer)
        headers["x-api-key"] = api_key
        # Also include Authorization for compatibility
        headers["Authorization"] = f"Bearer {api_key}"
    return headers

def query_graphql(query: str, variables: Optional[Dict] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Execute a GraphQL query."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers=get_headers(api_key),
        method='POST'
    )
    
    # Create SSL context (handles certificate verification)
    # Try default context first, fallback to unverified if needed
    ssl_context = ssl.create_default_context()
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except (ssl.SSLError, urllib.error.URLError) as e:
        # Check if it's an SSL certificate error
        if 'CERTIFICATE_VERIFY_FAILED' in str(e) or 'certificate' in str(e).lower():
            # Fallback to unverified context if default fails (for testing)
            print("⚠️  SSL certificate verification failed, using unverified context...")
            ssl_context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=ssl_context) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
        else:
            raise
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        raise

def get_titles(api_key: Optional[str] = None) -> Dict[str, Any]:
    """Get all available titles."""
    query = """
    query Titles {
        titles {
            id
            name
        }
    }
    """
    return query_graphql(query, api_key=api_key)

def get_tournaments(title_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Get tournaments for a specific title."""
    query = """
    query Tournaments($titleId: [ID!]!) {
        tournaments(filter: { title: { id: { in: $titleId } } }) {
            totalCount
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
    """
    variables = {"titleId": [title_id]}
    return query_graphql(query, variables, api_key=api_key)

def get_all_series(tournament_id: int, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Get all series for a tournament."""
    query = """
    query AllSeries($tournamentId: [ID!]!) {
        allSeries(
            filter: { tournament: { id: { in: $tournamentId }, includeChildren: { equals: true } } }
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
    """
    variables = {"tournamentId": [tournament_id]}
    return query_graphql(query, variables, api_key=api_key)

def explore_schema(api_key: Optional[str] = None) -> Dict[str, Any]:
    """Get GraphQL schema introspection to see what's available."""
    query = """
    query IntrospectionQuery {
        __schema {
            queryType {
                name
                fields {
                    name
                    description
                    type {
                        name
                        kind
                    }
                }
            }
        }
    }
    """
    return query_graphql(query, api_key=api_key)

def main():
    """Main exploration function."""
    import sys
    
    # Get API key (prioritizes .env file, then env var, then command line)
    api_key = get_api_key()
    
    print("=" * 60)
    print("Grid.gg Central Data API Explorer")
    print("=" * 60)
    print()
    
    if not api_key:
        print("⚠️  No API key found.")
        print("   Options:")
        print("   1. Create a .env file with: GRID_API_KEY=your-api-key-here")
        print("   2. Set environment variable: export GRID_API_KEY='your-api-key-here'")
        print("   3. Pass as argument: python3 api_explorer.py 'your-api-key-here'")
        print("   Attempting queries without authentication...")
        print()
    
    try:
        # 1. Get Titles
        print("📋 Step 1: Fetching available titles...")
        titles_result = get_titles(api_key)
        print(json.dumps(titles_result, indent=2))
        print()
        
        # Check for errors
        if "errors" in titles_result:
            print("❌ API returned errors:")
            for error in titles_result["errors"]:
                print(f"   - {error.get('message', 'Unknown error')}")
                if error.get('extensions', {}).get('errorType') == 'UNAUTHENTICATED':
                    print("\n💡 This API requires authentication.")
                    print("   Please set your API key:")
                    print("   export GRID_API_KEY='your-api-key-here'")
                    print("   Or pass it as an argument to the script.")
            return
        
        if "data" in titles_result and titles_result["data"] and titles_result["data"].get("titles"):
            titles = titles_result["data"]["titles"]
            print(f"✅ Found {len(titles)} titles")
            
            # Use first title or title ID "3" as mentioned in example
            if titles:
                title_id = "3" if any(t.get("id") == "3" for t in titles) else titles[0]["id"]
                print(f"📊 Using title ID: {title_id}")
                print()
                
                # 2. Get Tournaments
                print("🏆 Step 2: Fetching tournaments for title...")
                tournaments_result = get_tournaments(title_id, api_key)
                print(json.dumps(tournaments_result, indent=2))
                print()
                
                if "data" in tournaments_result and tournaments_result["data"].get("tournaments"):
                    tournaments = tournaments_result["data"]["tournaments"]
                    total_count = tournaments.get("totalCount", 0)
                    print(f"✅ Found {total_count} tournaments")
                    
                    if tournaments.get("edges"):
                        # Use first tournament
                        tournament_id = int(tournaments["edges"][0]["node"]["id"])
                        print(f"🎮 Using tournament ID: {tournament_id}")
                        print()
                        
                        # 3. Get Series
                        print("🎯 Step 3: Fetching series for tournament...")
                        series_result = get_all_series(tournament_id, api_key)
                        print(json.dumps(series_result, indent=2))
                        print()
                        
                        if "data" in series_result and series_result["data"].get("allSeries"):
                            series = series_result["data"]["allSeries"]
                            series_count = series.get("totalCount", 0)
                            print(f"✅ Found {series_count} series")
                            
                            if series.get("edges"):
                                print(f"\n📝 Sample Series IDs:")
                                for edge in series["edges"][:5]:  # Show first 5
                                    node = edge["node"]
                                    print(f"  - Series ID: {node['id']}")
                                    if node.get("teams"):
                                        team_names = [t["baseInfo"]["name"] for t in node["teams"] if t.get("baseInfo")]
                                        print(f"    Teams: {' vs '.join(team_names)}")
        
        # 4. Try schema introspection
        print("\n" + "=" * 60)
        print("🔍 Step 4: Exploring API Schema...")
        print("=" * 60)
        try:
            schema_result = explore_schema(api_key)
            if "data" in schema_result:
                query_type = schema_result["data"].get("__schema", {}).get("queryType", {})
                if query_type.get("fields"):
                    print("\n📚 Available Query Fields:")
                    for field in query_type["fields"]:
                        field_type = field.get("type", {})
                        type_name = field_type.get("name", "Unknown")
                        print(f"  - {field['name']}: {type_name}")
        except Exception as e:
            print(f"⚠️  Schema introspection failed: {e}")
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code}")
        if e.code == 401:
            print("   Authentication required. Please set GRID_API_KEY environment variable.")
        elif e.code == 403:
            print("   Access forbidden. Check API key permissions.")
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        print(f"   Response: {error_body}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

