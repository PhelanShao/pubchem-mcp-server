#!/usr/bin/env node

/**
 * Minimal MCP Server (JavaScript Version)
 * 
 * A simple implementation of the MCP protocol in JavaScript.
 */

// Enable strict mode
'use strict';

// Create basic logger
const fs = require('fs');
const path = require('path');
const os = require('os');

// Setup logging
const logDir = path.join(os.homedir(), '.mcp-logs');
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
}

const logFile = path.join(logDir, `mcp_js_${Date.now()}.log`);
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

function log(level, message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${level}] ${message}\n`;
    logStream.write(logMessage);
}

// Log startup
log('INFO', 'Starting JavaScript MCP server');

// Set up readline for reading from stdin
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: null, // Don't use readline for output
    terminal: false
});

// Handle requests
rl.on('line', (line) => {
    try {
        log('DEBUG', `Received input: ${line}`);
        
        // Parse the request
        const request = JSON.parse(line);
        const id = request.id;
        const method = request.method;
        
        log('DEBUG', `Parsed request: id=${id}, method=${method}`);
        
        // Create response based on method
        let response;
        
        if (method === 'initialize') {
            response = {
                jsonrpc: '2.0',
                id: id,
                result: {
                    name: 'pubchem-js-server',
                    version: '1.0.0',
                    capabilities: {
                        tools: {}
                    }
                }
            };
        } else if (method === 'list_tools') {
            response = {
                jsonrpc: '2.0',
                id: id,
                result: {
                    tools: [{
                        name: 'hello_world',
                        description: 'A simple hello world function',
                        inputSchema: {
                            type: 'object',
                            properties: {
                                name: {
                                    type: 'string',
                                    description: 'Your name'
                                }
                            }
                        }
                    }]
                }
            };
        } else if (method === 'call_tool') {
            const toolName = request.params?.name;
            const args = request.params?.arguments || {};
            
            if (toolName === 'hello_world') {
                const name = args.name || 'World';
                response = {
                    jsonrpc: '2.0',
                    id: id,
                    result: {
                        content: [{
                            type: 'text',
                            text: `Hello, ${name}!`
                        }]
                    }
                };
            } else {
                response = {
                    jsonrpc: '2.0',
                    id: id,
                    error: {
                        code: -32601,
                        message: `Method not found: ${toolName}`
                    }
                };
            }
        } else {
            response = {
                jsonrpc: '2.0',
                id: id,
                error: {
                    code: -32601,
                    message: `Method not found: ${method}`
                }
            };
        }
        
        // Send the response
        const responseJson = JSON.stringify(response);
        log('DEBUG', `Sending response: ${responseJson}`);
        
        process.stdout.write(responseJson + '\n');
        
        log('DEBUG', 'Response sent');
        
    } catch (error) {
        log('ERROR', `Error processing request: ${error.message}`);
        log('ERROR', error.stack);
        
        // Try to send an error response
        try {
            const errorResponse = {
                jsonrpc: '2.0',
                id: null,
                error: {
                    code: -32603,
                    message: `Internal error: ${error.message}`
                }
            };
            
            process.stdout.write(JSON.stringify(errorResponse) + '\n');
            
            log('DEBUG', 'Error response sent');
        } catch (e) {
            log('ERROR', `Failed to send error response: ${e.message}`);
        }
    }
});

// Handle end of input
rl.on('close', () => {
    log('INFO', 'End of input, shutting down');
    logStream.end();
    process.exit(0);
});

// Handle errors
process.on('uncaughtException', (error) => {
    log('ERROR', `Uncaught exception: ${error.message}`);
    log('ERROR', error.stack);
    
    // Try to clean up
    try {
        logStream.end();
    } catch (e) {
        // Nothing we can do
    }
    
    process.exit(1);
});

log('INFO', 'Server ready to process requests');
