# Claude Desktop MCP Configuration

## ✅ Correct Configuration

For Claude Desktop, use this configuration:

### Basic Setup

**Name:** `procurement-assistant`

**Command:** `uv`

**Arguments:** 
```
run backend/mcp_server.py
```

**Working Directory (if needed):**
```
d:/AI Projects/Procurement_Assistant
```

### Alternative: Using Full Path

If the above doesn't work, try:

**Command:** `uv`

**Arguments:**
```
--directory "d:/AI Projects/Procurement_Assistant" run backend/mcp_server.py
```

### Alternative: Using Python Directly

If `uv run` doesn't work, use Python directly:

**Command:** `python`

**Arguments:**
```
-m backend.mcp_server
```

**Working Directory:**
```
d:/AI Projects/Procurement_Assistant
```

## 🔍 Verification

After configuring, Claude Desktop should show:
- ✅ Status: **running** (green)
- ✅ Tools available: 10 tools
- ✅ Prompts available: 6 prompts
- ✅ Resources available: 2 resources

## 🧪 Testing in Claude Desktop

Once connected, you can test by asking Claude:

1. **"List all procurement files"** - Should use `list_procurement_files` tool
2. **"Analyze spend patterns"** - Should use `analyze_spend` tool
3. **"Run comprehensive procurement analysis"** - Should use `run_comprehensive_analysis` tool
4. **"What are the available procurement prompts?"** - Should list all 6 prompts

## 🐛 Troubleshooting

### Issue: Server not starting

**Check:**
1. Docker containers are running: `docker ps`
2. Ollama is running: `ollama list`
3. Check Claude Desktop logs (usually in AppData)

### Issue: "Module not found"

**Solution:** Ensure dependencies are installed:
```bash
cd "d:/AI Projects/Procurement_Assistant"
uv pip install -e .
```

### Issue: "Connection refused" to ChromaDB/MinIO

**Solution:** Start Docker services:
```bash
docker-compose up -d
```

### Issue: Tools not appearing

**Solution:**
1. Restart Claude Desktop
2. Check server status shows "running"
3. Verify command/arguments are correct
4. Check `mcp_server_debug.log` for errors

## 📝 Current Configuration (Your Setup)

Based on what you showed:
- ✅ Name: `procurement-assistant`
- ✅ Command: `uv`
- ⚠️ Arguments: `--directory d:/AI Projects/Procurement_Assistant run python backend/mcp_server.py`

**Note:** The `python` in the arguments might be redundant. Try:
```
--directory "d:/AI Projects/Procurement_Assistant" run backend/mcp_server.py
```

Or if you set the working directory separately, just use:
```
run backend/mcp_server.py
```

