# MCP Integration Guide

## Overview

The Procurement Assistant now includes a comprehensive **Model Context Protocol (MCP)** server that exposes procurement data and analysis capabilities to external MCP clients (like Claude Desktop, Cursor, etc.).

## What's Included

### 🛠️ MCP Tools (13 Tools)

#### File Management Tools
1. **`list_procurement_files()`** - Lists all procurement files stored in MinIO
2. **`get_file_info(filename)`** - Get information about a specific file

#### Data Querying Tools
3. **`query_procurement_data(query, n_results=5)`** - Search the procurement knowledge base using RAG

#### Agent-Based Analysis Tools
4. **`analyze_spend(query=None)`** - Run spend analysis using the Spend Analysis Agent
5. **`analyze_risk(query=None)`** - Run risk analysis using the Risk Monitoring Agent
6. **`analyze_suppliers(query=None)`** - Run supplier analysis using the Supplier Intelligence Agent
7. **`analyze_contracts(query=None)`** - Run contract analysis using the Contract Intelligence Agent
8. **`analyze_purchase_orders(query=None)`** - Run PO analysis using the PO Automation Agent
9. **`analyze_compliance(query=None)`** - Run compliance analysis using the Compliance & Policy Agent
10. **`run_comprehensive_analysis()`** - Run all 6 agents in parallel and return a comprehensive report

#### Advanced Analysis Tools
11. **`compare_suppliers(supplier1, supplier2)`** - Compare two suppliers side-by-side on delivery, quality, cost, and risk metrics
12. **`get_expiring_contracts(days_ahead=90)`** - Find contracts expiring within specified days with urgency alerts
13. **`export_report(report_type, format='excel')`** - Export analysis reports to Excel or CSV format

### 📦 MCP Resources

Resources expose procurement data files for direct access:
- **`procurement://files`** - Lists all available procurement files
- **`procurement://file/{filename}`** - Access specific file content

### 💬 MCP Prompts

Predefined prompt templates for common queries:
- **`prompt_spend_analysis`** - Template for spend analysis
- **`prompt_risk_assessment`** - Template for risk assessment
- **`prompt_supplier_performance`** - Template for supplier evaluation
- **`prompt_contract_review`** - Template for contract review
- **`prompt_compliance_check`** - Template for compliance checking
- **`prompt_executive_summary`** - Template for executive summary generation

## Running the MCP Server

### Standalone Mode

```bash
# Using uv (recommended)
uv run backend/mcp_server.py

# Or using python
python -m backend.mcp_server
```

The server will start and listen for MCP client connections via stdio.

### Testing the MCP Server

Run the test client:

```bash
uv run test_mcp.py
```

This will:
- List all available tools
- Test file listing
- Test data querying
- Test agent-based analysis
- List available prompts and resources

## Integration with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "procurement-assistant": {
      "command": "uv",
      "args": ["run", "backend/mcp_server.py"],
      "cwd": "/path/to/Procurement_Assistant"
    }
  }
}
```

### Cursor / Other MCP Clients

Configure the MCP server using stdio transport:
- **Command**: `uv` (or `python`)
- **Args**: `["run", "backend/mcp_server.py"]` (or `["-m", "backend.mcp_server"]`)
- **Working Directory**: Project root

## Usage Examples

### Example 1: List All Files

```python
# Via MCP client
files = await session.call_tool("list_procurement_files", arguments={})
```

### Example 2: Query Procurement Data

```python
# Search for risk-related information
result = await session.call_tool(
    "query_procurement_data", 
    arguments={"query": "high risk suppliers", "n_results": 5}
)
```

### Example 3: Run Spend Analysis

```python
# Run general spend analysis
result = await session.call_tool("analyze_spend", arguments={})

# Or with a specific query
result = await session.call_tool(
    "analyze_spend", 
    arguments={"query": "Analyze IT spend trends for Q4"}
)
```

### Example 4: Comprehensive Analysis

```python
# Run all analyses in parallel
report = await session.call_tool("run_comprehensive_analysis", arguments={})
```

### Example 5: Compare Suppliers

```python
# Compare two suppliers side-by-side
comparison = await session.call_tool(
    "compare_suppliers", 
    arguments={"supplier1": "Anadarko Supply Hub", "supplier2": "Occidental Resources"}
)
```

### Example 6: Get Expiring Contracts

```python
# Find contracts expiring in next 90 days
contracts = await session.call_tool(
    "get_expiring_contracts", 
    arguments={"days_ahead": 90}
)
```

### Example 7: Export Report

```python
# Export spend analysis to Excel
export_result = await session.call_tool(
    "export_report", 
    arguments={"report_type": "spend", "format": "excel"}
)

# Export comprehensive report (multiple sheets)
export_result = await session.call_tool(
    "export_report", 
    arguments={"report_type": "comprehensive", "format": "excel"}
)
```

## Architecture

```
┌─────────────────────┐
│   MCP Client        │  (Claude Desktop, Cursor, etc.)
│   (External)        │
└──────────┬──────────┘
           │ MCP Protocol (stdio)
           │
┌──────────▼──────────┐
│   MCP Server        │  (backend/mcp_server.py)
│   FastMCP           │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
┌───▼───┐   ┌─────▼─────┐   ┌───▼────┐
│ MinIO │   │ ChromaDB  │   │ Agents │
│ Files │   │ Vector DB │   │ (6)    │
└───────┘   └───────────┘   └────────┘
```

## Features

### ✅ Implemented
- 13 MCP tools covering all major functionality
- Supplier comparison tool for quick decision-making
- Contract expiry alerts for proactive risk management
- Report export to Excel/CSV for sharing and analysis
- File management operations
- RAG-based data querying
- Agent-based analysis (all 6 agents)
- Comprehensive analysis (parallel execution)
- Error handling and logging
- Lazy initialization for performance

### 🔄 Resources & Prompts
- Resources and prompts are defined but may need API adjustments based on FastMCP version
- Test with your MCP client to verify compatibility

## Error Handling

All tools include comprehensive error handling:
- Try-catch blocks around all operations
- Detailed error messages
- Logging to `mcp_server_debug.log`
- Graceful degradation on failures

## Performance

- **Lazy Initialization**: MinIO client and query engine are initialized only when needed
- **Parallel Execution**: Comprehensive analysis runs agents in parallel (max 2 workers)
- **Caching**: Vector store index is cached for faster subsequent queries

## Logging

Debug logs are written to `mcp_server_debug.log` with:
- Server startup/shutdown events
- Tool invocations
- Errors and exceptions
- Performance metrics

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are installed:
```bash
uv pip install -e .
```

### Issue: "Connection refused" to ChromaDB/MinIO
**Solution**: Start Docker services:
```bash
docker-compose up -d
```

### Issue: "Ollama connection refused"
**Solution**: Ensure Ollama is running:
```bash
ollama list  # Should show models
```

### Issue: Tools not appearing in MCP client
**Solution**: 
1. Check MCP server logs (`mcp_server_debug.log`)
2. Verify server is running: `uv run backend/mcp_server.py`
3. Check client configuration matches server command

## Next Steps

1. **Test with your MCP client** - Verify all tools work correctly
2. **Customize prompts** - Adjust prompt templates in `backend/mcp_server.py`
3. **Add more tools** - Extend functionality as needed
4. **Monitor performance** - Check logs for optimization opportunities

## Support

For issues or questions:
1. Check `mcp_server_debug.log` for detailed error messages
2. Verify all services are running (Docker, Ollama)
3. Test with `test_mcp.py` to isolate issues

---

**Happy Analyzing! 🚀**

