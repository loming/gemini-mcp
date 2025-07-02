#!/bin/bash
# Start health check server in background
python health_server.py &

# Start the actual MCP server
exec python run_server.py