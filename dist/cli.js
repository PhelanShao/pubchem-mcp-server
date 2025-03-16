#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const index_1 = require("./index");
// 处理命令行参数
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('Usage: pubchem-mcp <compound-name-or-cid> [format] [include_3d]');
    console.log('  format: JSON (default), CSV, or XYZ');
    console.log('  include_3d: true or false (default: false, required for XYZ format)');
    process.exit(1);
}
const query = args[0];
const format = args[1] || 'JSON';
const include3d = args[2] === 'true';
(0, index_1.getPubchemData)(query, format, include3d)
    .then(result => console.log(result))
    .catch(error => console.error('Error:', error));
