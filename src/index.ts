import { FastMCP } from "fastmcp";
import { spawn } from "child_process";
import { z } from "zod";

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 13001;

const server = new FastMCP({
  name: "Gemini Search Server",
  version: "1.0.0",
});

server.addTool({
  name: "query",
  description: "Send a query to an AI agent that can search real-time internet data and provide a second AI opinion",
  parameters: z.object({
    text: z.string().describe("The search query or question to send to the AI agent"),
  }),
  execute: async (args: { text: string }) => {
    return new Promise((resolve, reject) => {
      const process = spawn("gemini-cli", [], {
        stdio: ["pipe", "pipe", "pipe"],
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
        if (code === 0) {
          resolve(output.trim());
        } else {
          reject(new Error(`gemini-cli exited with code ${code}. Error: ${errorOutput}`));
        }
      });

      process.on("error", (err) => {
        reject(new Error(`Failed to spawn gemini-cli: ${err.message}`));
      });

      // Send the query text to the process
      process.stdin.write(args.text);
      process.stdin.end();
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
  
  server.start({
    transportType: "httpStream",
    httpStream: {
      port: PORT,
    },
  });
  
  console.log(`🚀 Gemini MCP Server starting on port ${PORT}`);
  console.log(`✅ Server running on http://localhost:${PORT}`);
  console.log(`💡 Press Ctrl+C to stop the server`);
}

main().catch((error) => {
  console.error('❌ Failed to start server:', error);
  process.exit(1);
});