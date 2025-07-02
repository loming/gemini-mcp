# Dockerfile for Gemini MCP Server
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies including UV
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install --no-cache-dir uv

# Create app directory
WORKDIR /app

# Copy Gemini MCP server files
COPY . .

# Install dependencies using UV
RUN uv pip install --system -r requirements.txt

# Install Gemini CLI tool (if available via pip)
RUN pip install --no-cache-dir google-generativeai || echo "Gemini CLI not available via pip"

# Health check and startup files are already copied with the '.' above

RUN chmod +x /app/start.sh /app/health_server.py

# Create non-root user for security
RUN groupadd -r gemini && useradd -r -g gemini gemini
RUN chown -R gemini:gemini /app
USER gemini

# Expose port
EXPOSE 8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8004/health || exit 1

# Run the startup script
CMD ["/app/start.sh"]