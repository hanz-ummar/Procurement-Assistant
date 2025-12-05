# MCP Setup Steps - Quick Guide

## 🚀 Prerequisites (Run These BEFORE Opening Claude Desktop)

### Step 1: Start Docker Services
```bash
cd "d:/AI Projects/Procurement_Assistant"
docker-compose up -d
```

**Verify:**
```bash
docker ps
```
Should show:
- `procurement_minio` (ports 9000, 9001)
- `procurement_chromadb` (port 8000)

### Step 2: Verify Ollama is Running
```bash
ollama list
```

Should show:
- `llama3.2:3b`
- `bge-m3:567m`

If not, start Ollama (usually runs automatically on Windows).

### Step 3: Verify Dependencies are Installed
```bash
cd "d:/AI Projects/Procurement_Assistant"
uv pip install -e .
```

## ✅ That's It!

**You DON'T need to:**
- ❌ Open the project in Cursor first
- ❌ Manually start the MCP server
- ❌ Run any Python commands
- ❌ Type any commands before launching Claude Desktop

## 🎯 What Happens Automatically

1. **You open Claude Desktop**
2. **Claude Desktop reads your MCP configuration**
3. **Claude Desktop automatically starts the MCP server** using:
   - Command: `uv`
   - Args: `--directory d:/AI Projects/Procurement_Assistant run python backend/mcp_server.py`
4. **MCP server connects to your backend** (ChromaDB, MinIO, Ollama)
5. **Tools become available** in Claude Desktop

## 📋 Daily Workflow

### First Time Setup (One-time):
1. ✅ Start Docker: `docker-compose up -d`
2. ✅ Verify Ollama: `ollama list`
3. ✅ Install dependencies: `uv pip install -e .`
4. ✅ Configure Claude Desktop (already done ✅)

### Daily Use:
1. **Start Docker** (if not running):
   ```bash
   docker-compose up -d
   ```
2. **Open Claude Desktop** - MCP server starts automatically!
3. **Start asking questions** - Tools are ready!

## 🔍 How to Verify MCP is Working

### Option 1: Check Claude Desktop UI
- Look for "procurement-assistant" in MCP servers list
- Status should show: **"running"** (green)

### Option 2: Ask Claude
```
"What MCP tools are available from procurement-assistant?"
```

Should list all 10 tools.

### Option 3: Test a Tool
```
"List all procurement files"
```

Should return your files.

## 🐛 Troubleshooting

### Issue: MCP server not starting in Claude Desktop

**Check:**
1. Docker is running: `docker ps`
2. Ollama is running: `ollama list`
3. Dependencies installed: `uv pip list | grep mcp`
4. Command path is correct in Claude Desktop config

### Issue: "Connection refused" errors

**Solution:**
```bash
# Restart Docker services
docker-compose down
docker-compose up -d

# Verify ports
docker ps
```

### Issue: "Module not found"

**Solution:**
```bash
cd "d:/AI Projects/Procurement_Assistant"
uv pip install -e . --force-reinstall
```

## 📝 Summary

**Before Claude Desktop:**
- ✅ Docker running (`docker-compose up -d`)
- ✅ Ollama running (usually automatic)
- ✅ Dependencies installed (one-time)

**Then:**
- ✅ Just open Claude Desktop
- ✅ MCP server starts automatically
- ✅ Start using tools!

**No need to:**
- ❌ Open Cursor
- ❌ Run Python scripts manually
- ❌ Start MCP server yourself

The MCP server is **automatically managed by Claude Desktop** based on your configuration!

