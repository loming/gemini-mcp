#!/usr/bin/env python3
"""
Simple health check server for Gemini MCP
"""
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Gemini MCP Server", version="1.0.0")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "service": "gemini-mcp"})

@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(content={
        "service": "Gemini MCP Server",
        "version": "1.0.0",
        "endpoints": ["/health"]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)