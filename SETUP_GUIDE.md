# 🚀 Procurement Assistant - Complete Setup Guide

This guide will help you set up and run the Procurement Assistant AI project on your local machine from scratch.

## 📋 Prerequisites

Before starting, ensure your computer meets these requirements:

- **Operating System**: Windows 10/11, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Internet Connection**: Required for downloading dependencies and models

---

## 🛠️ Step 1: Install Required Software

### 1.1 Install Python 3.11+

**Windows:**
1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   ```
   Should show: `Python 3.11.x` or higher

**macOS:**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

---

### 1.2 Install Docker Desktop

1. Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop
3. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

---

### 1.3 Install Ollama

**Windows:**
1. Download from [ollama.com/download](https://ollama.com/download)
2. Run the installer
3. Ollama will start automatically in the background

**macOS:**
```bash
brew install ollama
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

4. Verify Ollama is running:
   ```bash
   ollama --version
   ```

---

## 📥 Step 2: Get the Project Files

### Option A: Using Git (Recommended)

```bash
git clone <repository-url>
cd Procurement_Assistant
```

### Option B: Download ZIP

1. Download the project ZIP file
2. Extract to a folder (e.g., `C:\Projects\Procurement_Assistant`)
3. Open terminal/command prompt in that folder

---

## 🔧 Step 3: Download AI Models

This step downloads the required AI models (~4GB total). It may take 10-30 minutes depending on your internet speed.

```bash
ollama pull llama3.2:3b
ollama pull bge-m3:567m
```

**Verification:**
```bash
ollama list
```
You should see both models listed.

---

## 🐳 Step 4: Start Infrastructure Services

Start MinIO (file storage) and ChromaDB (vector database):

```bash
docker-compose up -d
```

**Verify containers are running:**
```bash
docker ps
```

You should see:
- `procurement_minio` (ports 9000, 9001)
- `procurement_chromadb` (port 8000)

---

## 📦 Step 5: Install Python Dependencies

### Option A: Using pip (Standard)

```bash
pip install -e .
```

### Option B: Using uv (Faster - if available)

```bash
pip install uv
uv pip install -e .
```

---

## 🚀 Step 6: Run the Application

### Windows:
```bash
run_app.bat
```

### macOS/Linux:
```bash
streamlit run app.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

---

## 📊 Step 7: Test the Application

1. **Upload a CSV file**:
   - Click "Upload New File" in the sidebar
   - Select a procurement CSV file
   - Click "Process & Ingest"

2. **Run Analysis**:
   - Click "🚀 Run All Analysis" button
   - Wait ~40-60 seconds for completion

3. **Explore Results**:
   - Navigate through tabs: Executive Summary, Dashboard, Spend Analysis, etc.
   - Use the chat interface at the bottom to ask questions

---

## 🔍 Troubleshooting

### Issue: "Ollama connection refused"

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not, start Ollama service
# Windows: Ollama starts automatically
# macOS/Linux:
ollama serve
```

---

### Issue: "Docker containers not starting"

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove old volumes (CAUTION: deletes data)
docker-compose down -v

# Start fresh
docker-compose up -d
```

---

### Issue: "Port already in use"

**Solution:**
```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8501

# macOS/Linux:
lsof -i :8501

# Kill the process or change Streamlit port:
streamlit run app.py --server.port=8502
```

---

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -e . --force-reinstall
```

---

### Issue: "Out of Memory" during analysis

**Solution:**
1. Close other applications
2. Reduce parallel workers in `app.py`:
   ```python
   # Line 158 in app.py
   with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
   ```

---

## 🛑 Stopping the Application

1. **Stop Streamlit**: Press `Ctrl+C` in the terminal

2. **Stop Docker containers**:
   ```bash
   docker-compose down
   ```

3. **Stop Ollama** (optional):
   - Windows: Quit from system tray
   - macOS/Linux: `Ctrl+C` if running in terminal

---

## 🔄 Restarting the Application

```bash
# 1. Start Docker services
docker-compose up -d

# 2. Start the app
run_app.bat  # Windows
# OR
streamlit run app.py  # macOS/Linux
```

---

## 📁 Project Structure

```
Procurement_Assistant/
├── app.py                    # Main Streamlit application
├── backend/
│   ├── agents.py            # AI agents (Spend, Risk, etc.)
│   ├── config.py            # Configuration settings
│   ├── database.py          # MinIO & ChromaDB clients
│   ├── ingestion.py         # Data preprocessing
│   └── llm.py               # Ollama LLM client
├── ui/
│   └── tabs.py              # UI rendering functions
├── docker-compose.yml       # Docker services configuration
├── pyproject.toml           # Python dependencies
├── run_app.bat              # Windows startup script
└── README.md                # Project overview
```

---

## 🎯 System Resource Usage

During normal operation:
- **RAM**: 4-8GB
- **CPU**: 50-80% (during analysis)
- **GPU**: Used if available (NVIDIA GPUs via Ollama)
- **Disk**: ~10GB (models + data)

---

## 🆘 Getting Help

If you encounter issues:

1. Check the terminal/console for error messages
2. Verify all services are running:
   ```bash
   docker ps
   ollama list
   ```
3. Check logs:
   ```bash
   docker-compose logs
   ```

---

## 🎉 Success Checklist

- ✅ Python 3.11+ installed
- ✅ Docker Desktop running
- ✅ Ollama installed and models downloaded
- ✅ Docker containers running (MinIO + ChromaDB)
- ✅ Python dependencies installed
- ✅ Application accessible at http://localhost:8501
- ✅ Can upload CSV and run analysis

---

## 📝 Notes

- **First run** may take longer as models load into memory
- **Analysis time**: ~40-60 seconds for comprehensive analysis
- **Data persistence**: Files and embeddings are stored in Docker volumes
- **Privacy**: Everything runs locally - no data leaves your machine

---

## 🔐 Default Credentials

**MinIO Web Console** (http://localhost:9001):
- Username: `minioadmin`
- Password: `minioadmin`

---

**Happy Analyzing! 🚀**
