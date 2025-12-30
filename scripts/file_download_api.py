#!/usr/bin/env python3
"""
Grid.gg File Download API Client
Lists and downloads event files and end state files for series.
"""

import json
import urllib.request
import urllib.parse
import ssl
import os
import sys
import zipfile
from typing import Dict, Any, Optional

# File Download API base URL
FILE_DOWNLOAD_BASE_URL = "https://api.grid.gg/file-download"

# Import shared utilities
sys.path.insert(0, os.path.dirname(__file__))
from utils import get_api_key

def get_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    """Get request headers with API key."""
    headers = {
        "Accept": "application/json",
    }
    if api_key:
        headers["x-api-key"] = api_key
    return headers

def make_request(url: str, api_key: Optional[str] = None, accept_binary: bool = False):
    """Make HTTP GET request and return response body and headers."""
    req = urllib.request.Request(url, headers=get_headers(api_key))
    
    if accept_binary:
        req.add_header("Accept", "application/zip, application/json, */*")
    
    ssl_context = ssl.create_default_context()
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            body = response.read()
            headers = dict(response.headers)
            return body, headers
    except (ssl.SSLError, urllib.error.URLError) as e:
        if 'CERTIFICATE_VERIFY_FAILED' in str(e) or 'certificate' in str(e).lower():
            ssl_context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=ssl_context) as response:
                body = response.read()
                headers = dict(response.headers)
                return body, headers
        else:
            raise
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        raise

def list_files(series_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """List all available files for a series."""
    url = f"{FILE_DOWNLOAD_BASE_URL}/list/{series_id}"
    body, _ = make_request(url, api_key)
    return json.loads(body.decode('utf-8'))

def download_file(url: str, api_key: Optional[str] = None, output_path: Optional[str] = None) -> str:
    """Download a file from a URL."""
    body, headers = make_request(url, api_key, accept_binary=True)
    
    # Get filename from Content-Disposition header or URL
    filename = output_path
    if not filename:
        content_disposition = headers.get("Content-Disposition", "")
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"\'')
        else:
            # Extract from URL
            filename = url.split("/")[-1]
            if "?" in filename:
                filename = filename.split("?")[0]
    
    if not filename:
        filename = "downloaded_file"
    
    with open(filename, 'wb') as f:
        f.write(body)
    
    return filename

def download_events_file(series_id: str, api_key: Optional[str] = None, output_dir: str = ".") -> Optional[str]:
    """Download the Series Events JSONL zip file."""
    url = f"{FILE_DOWNLOAD_BASE_URL}/events/grid/series/{series_id}"
    output_path = os.path.join(output_dir, f"events_{series_id}_grid.jsonl.zip")
    
    try:
        filename = download_file(url, api_key, output_path)
        return filename
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Events file not found for Series {series_id}")
        return None

def download_end_state_file(series_id: str, api_key: Optional[str] = None, output_dir: str = ".") -> Optional[str]:
    """Download the Series End State JSON file."""
    url = f"{FILE_DOWNLOAD_BASE_URL}/end-state/grid/series/{series_id}"
    output_path = os.path.join(output_dir, f"end_state_{series_id}_grid.json")
    
    try:
        filename = download_file(url, api_key, output_path)
        return filename
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ End state file not found for Series {series_id}")
        return None

def extract_jsonl(zip_path: str, output_dir: str = ".") -> Optional[str]:
    """Extract JSONL file from zip."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find JSONL file in zip
            jsonl_files = [f for f in zip_ref.namelist() if f.endswith('.jsonl')]
            if not jsonl_files:
                print("⚠️  No JSONL file found in zip")
                return None
            
            jsonl_file = jsonl_files[0]
            output_path = os.path.join(output_dir, os.path.basename(jsonl_file))
            zip_ref.extract(jsonl_file, output_dir)
            
            # Rename if needed
            if os.path.basename(jsonl_file) != os.path.basename(output_path):
                os.rename(os.path.join(output_dir, jsonl_file), output_path)
            
            return output_path
    except Exception as e:
        print(f"❌ Error extracting zip: {e}")
        return None

def print_file_status(file_info: Dict[str, Any]):
    """Print formatted file information."""
    file_id = file_info.get("id", "unknown")
    description = file_info.get("description", "Unknown")
    status = file_info.get("status", "unknown")
    filename = file_info.get("fileName", "unknown")
    
    # Status emoji mapping
    status_emoji = {
        "ready": "✅",
        "processing": "⏳",
        "match-not-started": "⏸️",
        "match-in-progress": "▶️",
        "file-not-available": "❌"
    }
    
    emoji = status_emoji.get(status, "❓")
    
    print(f"  {emoji} {file_id}: {description}")
    print(f"     Status: {status}")
    print(f"     File: {filename}")
    if status == "ready":
        print(f"     URL: {file_info.get('fullURL', 'N/A')}")
    print()

def main():
    # Get API key (prioritizes .env file, then env var, then command line)
    api_key = get_api_key()
    
    # Get series ID (now first argument since API key is optional)
    if len(sys.argv) > 1:
        # Check if first arg looks like a series ID (numeric) or API key
        first_arg = sys.argv[1]
        if first_arg.isdigit() or len(first_arg) > 20:  # Series IDs are usually numeric, API keys are long
            series_id = first_arg
        elif len(sys.argv) > 2:
            series_id = sys.argv[2]
        else:
            series_id = input("Enter Series ID: ").strip()
    else:
        series_id = input("Enter Series ID: ").strip()
    
    if not series_id:
        print("❌ No Series ID provided")
        return
    
    print(f"🔍 Checking available files for Series ID: {series_id}")
    print()
    
    try:
        # List available files
        result = list_files(series_id, api_key)
        files = result.get("files", [])
        
        if not files:
            print("❌ No files available for this series")
            return
        
        print("📁 Available Files:")
        print("=" * 70)
        for file_info in files:
            print_file_status(file_info)
        
        # Download ready files
        ready_files = [f for f in files if f.get("status") == "ready"]
        
        if not ready_files:
            print("⚠️  No files are ready for download yet")
            return
        
        print("📥 Downloading ready files...")
        print()
        
        downloaded_files = []
        
        for file_info in ready_files:
            file_id = file_info.get("id")
            full_url = file_info.get("fullURL")
            
            if not full_url:
                continue
            
            print(f"Downloading {file_id}...")
            
            if file_id == "events-grid":
                filename = download_events_file(series_id, api_key)
                if filename:
                    downloaded_files.append(filename)
                    print(f"  ✅ Downloaded: {filename}")
                    
                    # Extract JSONL if requested
                    if "--extract" in sys.argv:
                        print(f"  📦 Extracting JSONL...")
                        jsonl_path = extract_jsonl(filename)
                        if jsonl_path:
                            print(f"  ✅ Extracted: {jsonl_path}")
                            downloaded_files.append(jsonl_path)
            
            elif file_id == "state-grid":
                filename = download_end_state_file(series_id, api_key)
                if filename:
                    downloaded_files.append(filename)
                    print(f"  ✅ Downloaded: {filename}")
            
            else:
                # Generic download
                filename = download_file(full_url, api_key)
                downloaded_files.append(filename)
                print(f"  ✅ Downloaded: {filename}")
            
            print()
        
        if downloaded_files:
            print("=" * 70)
            print("✅ Download Summary:")
            for f in downloaded_files:
                size = os.path.getsize(f)
                print(f"  📄 {f} ({size:,} bytes)")
    
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Unauthorized. Check your API key.")
        elif e.code == 403:
            print("❌ Forbidden. You may not have access to this series.")
        elif e.code == 404:
            print(f"❌ Series {series_id} not found.")
        else:
            print(f"❌ HTTP Error {e.code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

