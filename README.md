# Gemini MCP Server

A Model Context Protocol (MCP) server that provides AI-powered internet search capabilities through the `gemini-cli` tool.

## Overview

This MCP server allows Claude and other AI assistants to perform real-time internet searches by interfacing with the `gemini-cli` command-line tool. It provides a single `query` tool that can search for current information and provide AI-powered analysis.

## Features

- **Real-time Search**: Query current internet data through AI-powered search
- **MCP Protocol**: Implements the Model Context Protocol for seamless integration
- **HTTP Streaming**: Uses HTTP streaming transport for efficient communication
- **TypeScript**: Fully typed with TypeScript for reliability
- **Graceful Shutdown**: Handles SIGINT/SIGTERM signals for clean exits

## Prerequisites

- Node.js 18+ 
- `gemini-cli` installed and configured on your system
- TypeScript (for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gemini-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Build the project:
```bash
npm run build
```

## Usage

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

The server will start on port 13001 by default, or you can set a custom port:
```bash
PORT=8080 npm start
```

## Configuration

### Environment Variables

- `PORT`: Server port (default: 13001)

### MCP Tool

The server provides one tool:

#### `query`
- **Description**: Send a query to an AI agent that can search real-time internet data
- **Parameters**:
  - `text` (string): The search query or question to send to the AI agent
- **Returns**: AI-generated response with current information

## Integration

### With Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "gemini-search": {
      "command": "node",
      "args": ["path/to/gemini-mcp/dist/index.js"],
      "env": {
        "PORT": "13001"
      }
    }
  }
}
```

### With Other MCP Clients

Connect to the HTTP streaming endpoint:
```
http://localhost:13001
```

## Development

### Scripts

- `npm run build` - Compile TypeScript to JavaScript
- `npm run start` - Run the compiled server
- `npm run dev` - Run in development mode with ts-node

### Project Structure

```
src/
├── index.ts          # Main server implementation
├── package.json      # Project configuration
└── dist/            # Compiled JavaScript (after build)
```

## Dependencies

- **fastmcp**: MCP server framework
- **zod**: Schema validation
- **child_process**: Node.js built-in for spawning processes

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request