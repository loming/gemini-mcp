# Gemini MCP Server

A Model Context Protocol (MCP) server that provides access to Google's Gemini AI through the `gemini-cli` command-line tool.

## Overview

This MCP server acts as a bridge between MCP-compatible clients (like Claude Desktop, Cursor, etc.) and the `gemini` command-line interface, allowing you to query Gemini AI models directly from your development environment.

## Prerequisites

### 1. Install Gemini CLI

First, you need to install the `gemini-cli` tool from here [official Gemini CLI repository](https://github.com/google-gemini/gemini-cli)

### 2. Test Gemini CLI

Verify the installation works:

```bash
echo "Hello, how are you?" | gemini
```

## Installation

### Clone and Setup

```bash
# Clone or navigate to the gemini-mcp directory
cd path/to/gemini-mcp

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### Running the Server Directly

```bash
# Run the MCP server
python server.py
```

### Testing the Server

```bash
# Run the test script
python test_gemini_server.py
```

## Client Configuration

### Claude Desktop

Add this configuration to your Claude Desktop settings file:

**Location of settings file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gemini-mcp": {
      "command": "{{PATH_TO_UV}}", // Run `which uv` and place the output here
      "args": [
        "--directory",
        "{{PATH_TO_SRC}}/gemini-mcp", // cd into the repo, run `pwd` and enter the output here + "/whatsapp-mcp-server"
        "run",
        "server.py"
      ]
    }
  }
}
```

### Cursor IDE

Add to your Cursor settings (`.cursor-settings/settings.json`):

```json
{
  "mcp.servers": {
    "gemini-mcp": {
      "command": "{{PATH_TO_UV}}", // Run `which uv` and place the output here
      "args": [
        "--directory",
        "{{PATH_TO_SRC}}/gemini-mcp", // cd into the repo, run `pwd` and enter the output here + "/whatsapp-mcp-server"
        "run",
        "server.py"
      ]
    }
  }
}
```

### Other MCP Clients

For any MCP-compatible client, use these connection details:

- **Command**: `python`
- **Args**: `["/path/to/gemini-mcp/server.py"]`

## Available Tools

### `query`

Process text prompts through Gemini AI.

**Parameters:**
- `prompt` (string): The text prompt to send to Gemini

**Example usage in Claude Desktop:**
```
Use the gemini-mcp server to ask: "Explain quantum computing in simple terms"
```

## Environment Variables

- Any environment variables supported by `gemini-cli`

## Troubleshooting

### Common Issues

1. **"The 'gemini' command is not found"**
   - Ensure `gemini-cli` is installed and in your PATH
   - Try running `which gemini` or `gemini --version`

2. **"Command failed with return code"**
   - Check if the gemini CLI is properly configured
   - Ensure you have internet connectivity
   - Verify your API quota isn't exceeded

### Debug Steps

1. Test the gemini command directly:
   ```bash
   echo "test prompt" | gemini
   ```

2. Run the server with verbose output:
   ```bash
   python server.py --verbose
   ```

## Development

### Project Structure

```
gemini-mcp/
├── server.py              # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── test_gemini_server.py  # Test script
└── README.md             # This file
```

### Architecture

- **FastMCP**: Uses FastMCP framework for MCP protocol implementation
- **Async Execution**: Non-blocking subprocess execution for performance
- **Error Handling**: Comprehensive error handling for various failure modes
- **Input Validation**: Prevents empty prompts and handles edge cases

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project follows the same license as the parent repository.

## Support

For issues related to:
- **This MCP server**: Create an issue in the repository
- **Gemini CLI**: Visit the [official Gemini CLI repository](https://github.com/google-gemini/gemini-cli)
- **MCP Protocol**: Check the [MCP specification](https://modelcontextprotocol.io/)