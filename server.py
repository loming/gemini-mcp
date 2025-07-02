#!/usr/bin/env python3
"""
Gemini MCP Server

A FastMCP server that provides a single 'query' function to process prompts
through a shell command called 'gemini'.
"""

import asyncio
import subprocess
from typing import Any

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("gemini-mcp")


@mcp.tool()
async def query(prompt: str) -> str:
    """
    Process a prompt through the 'gemini' shell command.
    
    Args:
        prompt: The text prompt to process
        
    Returns:
        The output from the gemini command
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    try:
        # Execute the gemini command with the prompt as input
        process = await asyncio.create_subprocess_exec(
            'gemini',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Send the prompt to the command's stdin (encode to bytes)
        stdout, stderr = await process.communicate(input=prompt.encode('utf-8'))
        
        # Check if the command was successful
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8').strip() if stderr else f"Command failed with return code {process.returncode}"
            raise RuntimeError(f"Gemini command failed: {error_msg}")
        
        return stdout.decode('utf-8').strip() if stdout else ""
        
    except FileNotFoundError:
        raise RuntimeError("The 'gemini' command is not found. Please ensure it's installed and in your PATH.")
    except Exception as e:
        raise RuntimeError(f"Error executing gemini command: {str(e)}")


if __name__ == "__main__":
    mcp.run()