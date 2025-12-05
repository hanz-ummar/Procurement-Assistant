import streamlit as st
import pandas as pd
from backend.ingestion import DataPreprocessingAgent
from backend.agents import (
    RAGRetrievalAgent, BaseDeepAgent, SpendAnalysisAgent, RiskMonitoringAgent,
    SupplierIntelligenceAgent, ContractIntelligenceAgent, POAutomationAgent,
    CompliancePolicyAgent
)
from ui.tabs import (
    render_executive_summary, render_dashboard, render_supplier_intelligence,
    render_spend_analysis, render_risk_monitoring, render_contract_intelligence,
    render_po_automation, render_compliance_policy
)

# Page Configuration with Custom Theme
st.set_page_config(
    page_title="Procurement Assistant AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/hanz-ummar/Procurement-Assistant',
        'Report a bug': 'https://github.com/hanz-ummar/Procurement-Assistant/issues',
        'About': '## Procurement Assistant AI\n\nAdvanced AI-powered procurement analytics with 9 specialized agents.'
    }
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    /* Main Theme Colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --background-color: #0e1117;
        --secondary-background: #262730;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #0e1117 100%);
        padding: 1rem 0.5rem;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    /* Sidebar Headers */
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        font-weight: 700;
        color: #ffffff;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-size: 1.1rem !important;
        color: #cccccc;
        margin-top: 1rem;
    }
    
    /* Buttons in Sidebar */
    [data-testid="stSidebar"] button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }
    
    /* Main Title */
    h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Tabs */
    [data-testid="stTabs"] {
        background: transparent;
    }
    
    [data-testid="stTabs"] button {
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
    }
    
    [data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(120deg, #1f77b4, #0066cc) !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    /* Cards and Containers */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        font-weight: 500;
    }
    
    /* Chat Interface */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        border-radius: 10px;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    }
    
    /* Dividers */
    hr {
        margin: 1.5rem 0;
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Select boxes and inputs */
    [data-testid="stSelectbox"], [data-testid="stTextInput"] {
        border-radius: 8px;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-active {
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    
    .status-pending {
        background: rgba(255, 152, 0, 0.2);
        color: #FF9800;
        border: 1px solid #FF9800;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "analysis_running" not in st.session_state:
    st.session_state.analysis_running = False

from backend.database import MinioClient
import io

# ============================================
# PROFESSIONAL SIDEBAR
# ============================================
with st.sidebar:
    # Logo and Title Section
    st.markdown("# 🤖 Procurement AI")
    st.caption("Advanced Analytics Platform")
    st.divider()
    
    # System Status Section
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.df is not None:
            st.markdown('<span class="status-badge status-active">● Active</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-pending">○ Idle</span>', unsafe_allow_html=True)
    with col2:
        data_rows = len(st.session_state.df) if st.session_state.df is not None else 0
        st.metric("Records", f"{data_rows:,}", label_visibility="collapsed")
    
    st.divider()
    
    # Data Source Section
    st.markdown("### 📁 Data Source")
    
    # Modern Tab-like Radio Buttons
    mode = st.radio(
        "Select Input Method",
        ["📤 Upload New", "📂 Load Existing"],
        label_visibility="collapsed",
        horizontal=False
    )
    
    st.markdown("")  # Spacer
    
    selected_file_content = None
    selected_file_name = None
    
    if mode == "📤 Upload New":
        # Upload Section with Better UX
        st.markdown("##### Upload Procurement Data")
        uploaded_file = st.file_uploader(
            "Drag and drop CSV file here",
            type=["csv"],
            help="Upload your procurement CSV file for analysis",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            selected_file_name = uploaded_file.name
            selected_file_content = uploaded_file.getvalue()
            
            # File Info
            file_size = len(selected_file_content) / 1024  # KB
            st.success(f"✓ **{selected_file_name}**  \n📦 {file_size:.1f} KB")
            
            st.markdown("")
            if st.button("🚀 Process & Analyze", type="primary", width="stretch"):
                progress_bar = st.progress(0, text="🔄 Initializing...")
                def update_progress(p, text):
                    progress_bar.progress(p, text=f"🔄 {text}")

                with st.spinner("Processing your data..."):
                    agent = DataPreprocessingAgent()
                    success, message = agent.process_csv(selected_file_content, selected_file_name, progress_callback=update_progress)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state.df = pd.read_csv(io.BytesIO(selected_file_content))
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")

    else:  # Load Existing
        st.markdown("##### Available Files")
        minio_client = MinioClient()
        files = minio_client.list_files()
        
        if files:
            selected_file_name = st.selectbox(
                "Choose a file",
                files,
                label_visibility="collapsed",
                help="Select from previously uploaded files"
            )
            
            st.markdown("")
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("📥 Load Data", width="stretch", type="primary"):
                    with st.spinner("📂 Loading..."):
                        content = minio_client.get_file_content(selected_file_name)
                        if content:
                            st.session_state.df = pd.read_csv(io.BytesIO(content))
                            st.success(f"✅ Loaded successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to load file")
            
            with col2:
                # Delete in expander
                with st.expander("🗑️"):
                    if st.button("Delete", type="secondary", width="stretch", help="Delete this file"):
                        with st.spinner("Deleting..."):
                            # Delete from MinIO
                            minio_success = minio_client.delete_file(selected_file_name)
                            
                            # Delete from ChromaDB
                            try:
                                import chromadb
                                from backend.config import Config
                                client = chromadb.HttpClient(host=Config.CHROMA_HOST, port=Config.CHROMA_PORT)
                                collection = client.get_collection("procurement_data")
                                collection.delete(where={"source": selected_file_name})
                                chroma_success = True
                            except Exception as e:
                                st.error(f"ChromaDB: {e}")
                                chroma_success = False
                            
                            if minio_success and chroma_success:
                                st.success("✅ Deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Delete failed")
        else:
            st.info("📭 No files available  \nUpload your first file to get started!")
    
    st.divider()
    
    # Analysis Control Section
    if st.session_state.df is not None:
        st.markdown("### 🎯 Analysis Control")
        
        # Big Analysis Button
        if st.button(
            "⚡ Run Complete Analysis",
            type="primary",
            width="stretch",
            help="Execute all 6 AI agents in parallel"
        ):
            import concurrent.futures
            import time
            
            st.session_state.analysis_running = True
            start_time = time.time()
            
            with st.spinner("🤖 AI Agents Working..."):
                # Initialize Agents
                agents = {
                    "spend": SpendAnalysisAgent(),
                    "risk": RiskMonitoringAgent(),
                    "supplier": SupplierIntelligenceAgent(),
                    "contract": ContractIntelligenceAgent(),
                    "po": POAutomationAgent(),
                    "compliance": CompliancePolicyAgent()
                }
                
                # Define tasks
                tasks = {
                    "spend": ("Analyze spend patterns, identifying anomalies and opportunities.", agents["spend"]),
                    "risk": ("Identify high-risk suppliers and potential supply chain disruptions.", agents["risk"]),
                    "supplier": ("Provide a detailed analysis of top suppliers and their performance.", agents["supplier"]),
                    "contract": ("Review contracts for expiry and compliance risks.", agents["contract"]),
                    "po": ("Analyze Purchase Orders for delays and price discrepancies.", agents["po"]),
                    "compliance": ("Check for policy violations and budget adherence.", agents["compliance"])
                }
                
                results = {}
                status_text = st.empty()
                progress_bar = st.progress(0)
                completed_count = 0
                total_tasks = len(tasks)

                def run_agent_task(key, query, agent):
                    return key, agent.run(query)

                # Execute in parallel
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_to_task = {
                        executor.submit(run_agent_task, key, query, agent): key 
                        for key, (query, agent) in tasks.items()
                    }
                    
                    for future in concurrent.futures.as_completed(future_to_task):
                        key, result = future.result()
                        results[key] = result
                        completed_count += 1
                        progress = completed_count / total_tasks
                        progress_bar.progress(progress)
                        status_text.text(f"✓ {completed_count}/{total_tasks} • {key.title()} Complete")

                # Store results
                st.session_state.spend_report = results["spend"]
                st.session_state.risk_report = results["risk"]
                st.session_state.supplier_report = results["supplier"]
                st.session_state.contract_report = results["contract"]
                st.session_state.po_report = results["po"]
                st.session_state.compliance_report = results["compliance"]
                
                # Executive Summary
                st.session_state.exec_summary_report = f"### Financial Overview\n{st.session_state.spend_report}\n\n### Risk Overview\n{st.session_state.risk_report}"
                
                end_time = time.time()
                duration = end_time - start_time
                minutes, seconds = divmod(duration, 60)
                
                status_text.empty()
                progress_bar.empty()
                st.success(f"✅ Analysis Complete! ({int(minutes)}m {int(seconds)}s)")
                st.balloons()
                st.session_state.analysis_running = False
        
        st.divider()
    
    # Settings Section
    with st.expander("⚙️ Settings & Tools", expanded=False):
        st.markdown("##### Quick Actions")
        
        if st.button("🔄 Refresh Data", width="stretch"):
            st.rerun()
        
        if st.button("🗑️ Clear All", width="stretch", type="secondary"):
            st.session_state.df = None
            st.session_state.messages = []
            keys_to_clear = [
                "spend_report", "risk_report", "supplier_report", 
                "contract_report", "po_report", "compliance_report", 
                "exec_summary_report"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("✅ Dashboard cleared!")
            st.rerun()
    
    st.divider()
    
    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.75rem; padding: 1rem 0;'>
            <p style='margin: 0;'><strong>Procurement Assistant AI</strong></p>
            <p style='margin: 0.25rem 0;'>v2.0 • Enterprise Edition</p>
            <p style='margin: 0.25rem 0;'>Powered by Llama 3.2 & RAG</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT AREA
# ============================================

# Header with Subtitle
st.markdown("# 🚀 Procurement Assistant AI")
st.markdown("**Enterprise Analytics Platform** • Real-time Insights • AI-Powered Decision Making")
st.divider()

if st.session_state.df is not None:
    # Enhanced Tab Interface
    tabs = st.tabs([
        "📊 Executive Summary",
        "📈 Dashboard", 
        "🏢 Suppliers",
        "💰 Spend Analysis",
        "⚠️ Risk & Alerts",
        "📦 PO Insights",
        "📄 Contracts",
        "✅ Compliance"
    ])
    
    with tabs[0]:
        render_executive_summary(st.session_state.df)
    with tabs[1]:
        render_dashboard(st.session_state.df)
    with tabs[2]:
        render_supplier_intelligence(st.session_state.df)
    with tabs[3]:
        render_spend_analysis(st.session_state.df)
    with tabs[4]:
        render_risk_monitoring(st.session_state.df)
    with tabs[5]:
        render_po_automation(st.session_state.df)
    with tabs[6]:
        render_contract_intelligence(st.session_state.df)
    with tabs[7]:
        render_compliance_policy(st.session_state.df)

else:
    # Welcome Screen with Better Design
    st.markdown("")
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 3rem 0;'>
                <h2 style='color: #1f77b4; font-size: 2rem;'>👋 Welcome to Procurement Assistant AI</h2>
                <p style='font-size: 1.2rem; color: #666; margin: 1rem 0;'>
                    Your intelligent procurement analytics platform powered by AI
                </p>
                <div style='background: rgba(31, 119, 180, 0.1); padding: 2rem; border-radius: 15px; margin: 2rem 0;'>
                    <h3 style='color: #1f77b4;'>🚀 Get Started</h3>
                    <p style='font-size: 1rem; line-height: 1.6;'>
                        Upload your procurement CSV file using the sidebar to unlock:<br><br>
                        ✓ Real-time analytics<br>
                        ✓ AI-powered insights<br>
                        ✓ Risk detection<br>
                        ✓ Supplier intelligence<br>
                        ✓ Compliance monitoring
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# CHAT INTERFACE (Modern Design)
# ============================================
@st.fragment
def render_chat_interface():
    st.divider()
    st.markdown("### 💬 AI Assistant")
    st.caption("Ask questions about your procurement data")

    # Chat History
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("💭 Ask about your procurement data...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤔 Analyzing..."):
                    class GeneralAssistant(BaseDeepAgent):
                        def __init__(self):
                            super().__init__("General Assistant", "Helpful assistant for procurement queries.")
                        
                        def run(self, query: str) -> str:
                            project_context = "Procurement Assistant Application"
                            try:
                                with open("README.md", "r", encoding="utf-8") as f:
                                    project_context = f.read()
                            except Exception:
                                pass

                            prompt = f"""
                            Answer the user's question based on the provided procurement data and project context.
                            
                            Project Context:
                            {project_context}

                            Data Context:
                            {{context}}
                            
                            User Query: {{query}}
                            """
                            return self._generate_insight(query, prompt)

                    agent = GeneralAssistant()
                    response = agent.run(prompt)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

render_chat_interface()
