import { FastMCP } from "fastmcp";
import { spawn } from "child_process";
import { z } from "zod";

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 13001;

const server = new FastMCP({
  name: "Gemini Search Server",
  version: "1.0.0",
  health: {
    // Enable / disable (default: true)
    enabled: true,
    // Body returned by the endpoint (default: 'ok')
    message: "healthy",
    // Path that should respond (default: '/health')
    path: "/health",
    // HTTP status code to return (default: 200)
    status: 200,
  },
  ping: {
    enabled: true,
    intervalMs: 25000, // 25s - optimal balance
    logLevel: "info" // enable monitoring
  },
});

server.addTool({
  name: "query",
  description: "Search on internet for real-time information",
  parameters: z.object({
    text: z.string().describe("The search query or question to send to the AI agent"),
  }),
  execute: async (args: { text: string }) => {
    console.log(`📝 Received query: ${args.text.substring(0, 100)}...`);
    return new Promise((resolve, reject) => {
      // Validate input
      if (!args.text || args.text.trim() === '') {
        reject(new Error('Query text cannot be empty'));
        return;
      }

      const process = spawn("gemini", [], {
        stdio: ["pipe", "pipe", "pipe"],
        timeout: 30000, // 30 second timeout
      });

      let output = "";
      let errorOutput = "";

      process.stdout.on("data", (data) => {
        output += data.toString();
      });

      process.stderr.on("data", (data) => {
        errorOutput += data.toString();
      });

      process.on("close", (code) => {
        clearTimeout(timeoutId);
        if (code === 0) {
          const result = output.trim() || "No response from Gemini CLI";
          console.log(`✅ Query completed successfully (${result.length} characters)`);
          resolve(result);
        } else {
          const errorMsg = `gemini-cli exited with code ${code}. Error: ${errorOutput || 'Unknown error'}`;
          console.error(`❌ Query failed: ${errorMsg}`);
          reject(new Error(errorMsg));
        }
      });

      process.on("error", (err) => {
        reject(new Error(`Failed to spawn gemini-cli: ${err.message}. Make sure gemini-cli is installed and available in PATH.`));
      });

      // Set a timeout for the process
      const timeoutId = setTimeout(() => {
        process.kill();
        reject(new Error('Gemini CLI query timed out after 30 seconds'));
      }, 30000);

      process.on('exit', () => {
        clearTimeout(timeoutId);
      });

      // Send the query text to the process
      try {
        process.stdin.write(args.text);
        process.stdin.end();
      } catch (err) {
        clearTimeout(timeoutId);
        reject(new Error(`Failed to write to gemini-cli: ${err}`));
      }
    });
  },
});

function setupGracefulShutdown() {
  process.on('SIGINT', () => {
    console.log('\n👋 Gracefully shutting down Gemini MCP Server...');
    process.exit(0);
  });

  process.on('SIGTERM', () => {
    console.log('\n👋 Gracefully shutting down Gemini MCP Server...');
    process.exit(0);
  });
}

async function main() {
  setupGracefulShutdown();
  
  try {
    await server.start({
      transportType: "httpStream",
      httpStream: {
        port: PORT,
        endpoint: "/mcp"
      },
    });
    
    console.log(`🚀 Gemini MCP Server started successfully`);
    console.log(`✅ Server running on http://localhost:${PORT}/mcp`);
    console.log(`🛠️ Available tools: query`);
    console.log(`💡 Press Ctrl+C to stop the server`);
  } catch (error) {
    console.error('❌ Failed to start Gemini MCP Server:', error);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error('❌ Failed to start server:', error);
  process.exit(1);
});