#!/bin/bash
cd "/Users/robert.lee/GithubProjects/mcp-sequential-thinking"
source .venv/bin/activate
exec python run_server.py "$@"
