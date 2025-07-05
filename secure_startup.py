#!/usr/bin/env python3
"""
Secure startup wrapper for mcp-sequential-thinking MCP server
"""

import sys
import os
from pathlib import Path

# Add security policy to path
sys.path.insert(0, str(Path(__file__).parent))

# Import security policy first
try:
    import security_policy
    print("✅ Security policy loaded for mcp-sequential-thinking")
except ImportError:
    print("⚠️  Security policy not found")

# Set environment restrictions
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONHASHSEED'] = '0'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Restrict Python path
if 'PYTHONPATH' in os.environ:
    allowed_paths = [
        str(Path.home() / 'GithubProjects'),
        '/usr/local/lib/python3.10/site-packages',
        '/usr/lib/python3.10'
    ]
    current_paths = os.environ['PYTHONPATH'].split(':')
    safe_paths = [p for p in current_paths if any(p.startswith(ap) for ap in allowed_paths)]
    os.environ['PYTHONPATH'] = ':'.join(safe_paths)

print(f"🔒 Starting mcp-sequential-thinking with security restrictions")

# Import and run the actual server
if __name__ == "__main__":
    # Add your server's main module import here
    print("🚀 mcp-sequential-thinking MCP server starting...")
