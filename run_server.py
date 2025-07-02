#!/usr/bin/env python3
"""
Gemini MCP Server Startup Script

This script starts the Gemini MCP server with proper error handling and logging.
Can be run directly with python or uv.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the server
try:
    from server import mcp
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("  pip install fastmcp pydantic httpx mcp typer")
    print("  or: uv pip install --system -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Gemini MCP Server...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Gemini MCP Server stopped by user")
    except Exception as e:
        print(f"❌ Gemini MCP Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)