# PubChem MCP Server

A Model Context Protocol (MCP) server for retrieving PubChem compound data.

## Features

- Supports query by compound name or CID
- Provides multiple output formats: JSON, CSV, XYZ
- Supports 3D structure data retrieval and conversion
- Local caching system to reduce API calls
- Automatic retry mechanism for improved reliability

## Installation

```bash
npm install -g @modelcontextprotocol/server-pubchem
```

## Configuration

Add the following configuration to your MCP settings file:

```json
{
  "mcpServers": {
    "pubchem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-pubchem"]
    }
  }
}
```

## Usage

The server provides the following tools:

### get_pubchem_data

Retrieve compound structure and property data.

Parameters:
- `query`: (Required) Compound name or PubChem CID
- `format`: (Optional) Output format, options: "JSON", "CSV", or "XYZ", default: "JSON"
- `include_3d`: (Optional) Whether to include 3D structure information (only valid when format is "XYZ"), default: false

Examples:

```python
# Get data in JSON format
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin"
})

# Get data in CSV format
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin",
    "format": "CSV"
})

# Get 3D structure data in XYZ format
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin",
    "format": "XYZ",
    "include_3d": True
})
```

## Caching

- Property data is cached in memory
- 3D structure data (XYZ format) is cached in `~/.pubchem-mcp/cache` directory
- Cache file name format: `[CID].xyz`

## Dependencies

- @modelcontextprotocol/sdk
- axios
- rdkit-js (optional, for enhanced 3D structure generation)

**Note:** While rdkit-js is listed as a dependency, the server can still function without it. When rdkit-js is not available, the server will fall back to using PubChem's 3D structure data directly, with a simplified SDF parser for XYZ format conversion.

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test
```

## License

MIT
