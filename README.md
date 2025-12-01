# Procurement Assistant AI 🤖

A high-performance, Agentic AI system designed to automate procurement data analysis. This application ingests raw procurement data (CSV), uses a **RAG (Retrieval-Augmented Generation)** architecture to understand it, and deploys **9 specialized AI Agents** to generate actionable insights on Spend, Risk, Supplier Performance, and Compliance.

## 🚀 Key Features

*   **Multi-Agent Architecture:** Deploys 9 specialized agents (7 Deep Reasoning, 2 Utility) to analyze data from multiple angles simultaneously.
*   **RAG-Powered Insights:** Uses **LlamaIndex** and **ChromaDB** to retrieve the most relevant data chunks (Top-K=4) for accurate, context-aware answers.
*   **Local LLM Privacy:** Runs entirely offline using **Ollama** (Llama 3.2:3b) for maximum data security and zero cost.
*   **High-Performance Analysis:** Optimized for local hardware (Ryzen 7 / RTX 4060), completing a full comprehensive analysis in **~40 seconds**.
*   **Interactive Dashboard:** Built with **Streamlit**, featuring dynamic charts, detailed reports, and a persistent **AI Chat Assistant**.
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

1.  **Upload Data:** Upload your procurement CSV file (supports 3000+ rows).
2.  **Run Analysis:** Click "🚀 Run All Analysis" to trigger the agent swarm.
3.  **Explore Insights:** Navigate through the tabs (Spend, Risk, Supplier, etc.) to view detailed reports.
4.  **Chat with AI:** Use the chat interface at the bottom to ask specific questions like *"Which supplier has the best delivery rate?"*.
