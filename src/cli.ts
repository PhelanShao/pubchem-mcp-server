#!/usr/bin/env node
import { getPubchemData } from './index';

// 处理命令行参数
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: pubchem-mcp <compound-name-or-cid> [format]');
  process.exit(1);
}

const query = args[0];
const format = args[1] || 'JSON';

getPubchemData(query, format)
  .then(result => console.log(result))
  .catch(error => console.error('Error:', error));
