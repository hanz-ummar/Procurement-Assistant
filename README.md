# Procurement Assistant AI 🤖

[![Tests](https://github.com/hanz-ummar/Procurement-Assistant/actions/workflows/tests.yml/badge.svg)](https://github.com/hanz-ummar/Procurement-Assistant/actions/workflows/tests.yml)
[![Code Quality](https://github.com/hanz-ummar/Procurement-Assistant/actions/workflows/code-quality.yml/badge.svg)](https://github.com/hanz-ummar/Procurement-Assistant/actions/workflows/code-quality.yml)
[![codecov](https://codecov.io/gh/hanz-ummar/Procurement-Assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/hanz-ummar/Procurement-Assistant)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, **fully-tested** Agentic AI system designed to automate procurement data analysis. This application ingests raw procurement data (CSV), uses a **RAG (Retrieval-Augmented Generation)** architecture to understand it, and deploys **9 specialized AI Agents** to generate actionable insights on Spend, Risk, Supplier Performance, and Compliance.

**✅ 63 Automated Tests | 100% Pass Rate | Production-Ready**

## 🚀 Key Features

*   **Multi-Agent Architecture:** Deploys 9 specialized agents (7 Deep Reasoning, 2 Utility) to analyze data from multiple angles simultaneously.
*   **RAG-Powered Insights:** Uses **LlamaIndex** and **ChromaDB** to retrieve the most relevant data chunks (Top-K=4) for accurate, context-aware answers.
*   **Local LLM Privacy:** Runs entirely offline using **Ollama** (Llama 3.2:3b) for maximum data security and zero cost.
*   **High-Performance Analysis:** Optimized for local hardware (Ryzen 7 / RTX 4060), completing a full comprehensive analysis in **~40 seconds**.
*   **Interactive Dashboard:** Built with **Streamlit**, featuring dynamic charts, detailed reports, and a persistent **AI Chat Assistant**.
*   **MCP Integration:** Full **Model Context Protocol (MCP)** support for integration with Claude Desktop and other AI assistants - 10 tools, 6 prompts, and resources.
*   **Scalable Infrastructure:** Uses **MinIO** for object storage and **Docker** for easy deployment.

## 🛠️ Tech Stack

*   **Frontend:** Streamlit
*   **Backend Framework:** LlamaIndex
*   **LLM Server:** Ollama (Model: `llama3.2:3b`, Embeddings: `bge-m3:567m`)
*   **Vector Database:** ChromaDB (Dockerized)
*   **Object Storage:** MinIO (Dockerized)
*   **Language:** Python 3.11+

## 🧠 The 9 AI Agents

1.  **Spend Analysis Agent:** Identifies financial trends, anomalies, and cost-saving opportunities.
2.  **Risk Monitoring Agent:** Flags high-risk suppliers and potential supply chain disruptions.
3.  **Supplier Intelligence Agent:** Ranks suppliers based on delivery and quality performance.
4.  **Contract Intelligence Agent:** Reviews contracts for expiry dates and compliance risks.
5.  **PO Automation Agent:** Analyzes Purchase Orders for delivery delays and price discrepancies.
6.  **Compliance & Policy Agent:** Checks for policy violations and budget deviations.
7.  **General Assistant:** A chatbot that answers natural language questions about your data.
8.  **Data Preprocessing Agent:** Handles CSV ingestion, cleaning, and chunking.
9.  **RAG Retrieval Agent:** Manages vector search and data retrieval.

## ⚙️ Optimization Highlights

*   **Parallel Execution:** Runs 2 agents concurrently to maximize speed without overloading RAM (16GB limit).
*   **Context Optimization:** Limits LLM context to 4096 tokens to prevent OOM errors.
*   **Enhanced Retrieval:** Retrieves the top 4 most relevant data chunks (`k=4`) for richer, more accurate insights.
*   **Index Caching:** Implements Singleton pattern for the Vector Index to eliminate startup latency.

## 📦 Installation & Setup

1.  **Prerequisites:**
    *   Docker Desktop installed and running.
    *   Ollama installed with `llama3.2:3b` and `bge-m3:567m` pulled.
    *   Python 3.11+

2.  **Start Infrastructure:**
    ```bash
    docker-compose up -d
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Application:**
    ```bash
    run_app.bat
    ```

## 📊 Usage

### Streamlit Web Interface

1.  **Upload Data:** Upload your procurement CSV file (supports 3000+ rows).
2.  **Run Analysis:** Click "🚀 Run All Analysis" to trigger the agent swarm.
3.  **Explore Insights:** Navigate through the tabs (Spend, Risk, Supplier, etc.) to view detailed reports.
4.  **Chat with AI:** Use the chat interface at the bottom to ask specific questions like *"Which supplier has the best delivery rate?"*.

### MCP Integration (Claude Desktop)

The project includes a full MCP server with 10 tools for integration with Claude Desktop and other MCP clients.

**Quick Start:**
1. Start Docker: `docker-compose up -d`
2. Configure Claude Desktop (see `CLAUDE_DESKTOP_SETUP.md`)
3. Open Claude Desktop - MCP server starts automatically
4. Ask questions like: *"List all procurement files"* or *"Run comprehensive procurement analysis"*

**Available MCP Tools (13 tools):**
- File management (list files, get file info)
- Data querying (RAG-based search)
- Agent analysis (spend, risk, suppliers, contracts, PO, compliance)
- Comprehensive analysis (all agents in parallel)
- **Supplier comparison** (side-by-side metrics)
- **Contract expiry alerts** (proactive risk management)
- **Report export** (Excel/CSV format)

See `MCP_INTEGRATION.md` for detailed documentation.

## 📚 Documentation

- **`SETUP_GUIDE.md`** - Complete setup instructions
- **`MCP_INTEGRATION.md`** - MCP server documentation
- **`CLAUDE_DESKTOP_SETUP.md`** - Claude Desktop configuration
- **`MCP_SETUP_STEPS.md`** - Quick MCP setup guide
- **`REMOTE_ACCESS_GUIDE.md`** - Sharing project remotely
- **`SHARE_WITH_NGROK.md`** - Share Streamlit app via ngrok
