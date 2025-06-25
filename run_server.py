#!/usr/bin/env python3
"""
Gemini MCP Server Startup Script

This script starts the Gemini MCP server with proper error handling and logging.
Can be run directly with uv or python.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the server
from server import mcp

if __name__ == "__main__":
    print("🚀 Starting Gemini MCP Server...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Gemini MCP Server stopped by user")
    except Exception as e:
        print(f"❌ Gemini MCP Server error: {e}")
        sys.exit(1)