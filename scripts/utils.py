#!/usr/bin/env python3
"""
Shared utilities for Grid.gg API scripts.
"""

import os
import sys
from typing import Optional

def load_env_file(env_path: str = ".env") -> dict:
    """
    Load environment variables from .env file.
    Looks for .env in current directory or project root.
    """
    env_vars = {}
    
    # Try current directory first
    paths_to_try = [
        env_path,  # Current directory
        os.path.join(os.path.dirname(os.path.dirname(__file__)), env_path),  # Project root
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            # Remove quotes if present
                            value = value.strip('"\'')
                            env_vars[key.strip()] = value
                break  # Successfully loaded, stop trying
            except Exception as e:
                # Continue to next path if this one fails
                continue
    
    return env_vars

def get_api_key(require_key: bool = True) -> Optional[str]:
    """
    Get API key from multiple sources, in priority order:
    1. .env file (project file) - HIGHEST PRIORITY
    2. Environment variable (GRID_API_KEY)
    3. Command line argument (sys.argv[1]) - LOWEST PRIORITY (override)
    
    Args:
        require_key: If True, print error and exit if no key found
    
    Returns:
        API key string or None if not found and require_key=False
    """
    api_key = None
    
    # Priority 1: .env file (project file)
    env_vars = load_env_file()
    api_key = env_vars.get("GRID_API_KEY")
    
    # Priority 2: Environment variable
    if not api_key:
        api_key = os.getenv("GRID_API_KEY")
    
    # Priority 3: Command line argument (as override/fallback)
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key and require_key:
        print("❌ No API key found!")
        print()
        print("Please set your API key in one of these ways:")
        print()
        print("  1. Create a .env file in the project root:")
        print("     GRID_API_KEY=your-api-key-here")
        print()
        print("  2. Set environment variable:")
        print("     export GRID_API_KEY='your-api-key-here'")
        print()
        print("  3. Pass as command line argument (not recommended):")
        print("     python3 script.py your-api-key-here")
        print()
        sys.exit(1)
    
    return api_key

