#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { getPubchemData } from './index';
import { ToolInput } from './types';

class PubChemServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'pubchem-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    
    // 错误处理
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'get_pubchem_data',
          description: '检索化合物结构和属性数据',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: '化合物名称或PubChem CID',
              },
              format: {
                type: 'string',
                description: '输出格式，选项："JSON"、"CSV"或"XYZ"，默认："JSON"',
                enum: ['JSON', 'CSV', 'XYZ'],
              },
              include_3d: {
                type: 'boolean',
                description: '是否包含3D结构信息（仅当format为"XYZ"时有效），默认：false',
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name !== 'get_pubchem_data') {
        throw new McpError(
          ErrorCode.MethodNotFound,
          `未知工具: ${request.params.name}`
        );
      }

      const args = request.params.arguments as unknown as ToolInput;
      
      if (!args.query) {
        throw new McpError(
          ErrorCode.InvalidParams,
          '缺少必需的参数: query'
        );
      }

      try {
        // 检查XYZ格式是否需要include_3d参数
        if (args.format?.toUpperCase() === 'XYZ' && !args.include_3d) {
          return {
            content: [
              {
                type: 'text',
                text: '使用XYZ格式时，include_3d参数必须设置为true',
              },
            ],
            isError: true,
          };
        }

        const result = await getPubchemData(args.query, args.format, args.include_3d);
        
        return {
          content: [
            {
              type: 'text',
              text: result,
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: 'text',
              text: `错误: ${error.message || '未知错误'}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('PubChem MCP服务器正在通过stdio运行');
  }
}

// 启动服务器
const server = new PubChemServer();
server.run().catch(console.error);
