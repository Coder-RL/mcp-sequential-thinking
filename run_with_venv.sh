#!/bin/bash
cd "/Users/robertlee/GitHubProjects/mcp-sequential-thinking"
source .venv/bin/activate
exec python run_server.py "$@"
