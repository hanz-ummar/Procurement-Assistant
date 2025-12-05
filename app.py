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

st.set_page_config(page_title="Procurement Assistant", layout="wide")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None

from backend.database import MinioClient
import io

# Sidebar - File Upload & Selection
with st.sidebar:
    st.title("📂 Data Management")
    
    # Mode Selection
    mode = st.radio("Source", ["Upload New File", "Select Existing File"])
    
    selected_file_content = None
    selected_file_name = None
    
    if mode == "Upload New File":
        uploaded_file = st.file_uploader("Upload Procurement CSV", type=["csv"])
        if uploaded_file:
            selected_file_name = uploaded_file.name
            selected_file_content = uploaded_file.getvalue()
            
            if st.button("Process & Ingest"):
                progress_bar = st.progress(0, text="Starting ingestion...")
                def update_progress(p, text):
                    progress_bar.progress(p, text=text)

                with st.spinner("Ingesting and analyzing data..."):
                    agent = DataPreprocessingAgent()
                    success, message = agent.process_csv(selected_file_content, selected_file_name, progress_callback=update_progress)
                    
                    if success:
                        st.success(message)
                        st.session_state.df = pd.read_csv(io.BytesIO(selected_file_content))
                    else:
                        st.error(message)

    else: # Select Existing File
        minio_client = MinioClient()
        files = minio_client.list_files()
        
        if files:
            selected_file_name = st.selectbox("Select a file", files)
            
            if st.button("Load File", width="stretch"):
                with st.spinner("Loading data..."):
                    content = minio_client.get_file_content(selected_file_name)
                    if content:
                        st.session_state.df = pd.read_csv(io.BytesIO(content))
                        st.success(f"Loaded {selected_file_name}")
                    else:
                        st.error("Failed to load file content.")
            
            # Use an expander for destructive actions to keep UI clean
            with st.expander("🗑️ Manage File", expanded=False):
                if st.button("Delete File", type="primary", width="stretch"):
                    with st.spinner("Deleting file..."):
                        # Delete from MinIO
                        minio_success = minio_client.delete_file(selected_file_name)
                        
                        # Delete from ChromaDB
                        try:
                            import chromadb
                            from backend.config import Config
                            client = chromadb.HttpClient(host=Config.CHROMA_HOST, port=Config.CHROMA_PORT)
                            collection = client.get_collection("procurement_data")
                            # Delete where source == selected_file_name
                            collection.delete(where={"source": selected_file_name})
                            chroma_success = True
                        except Exception as e:
                            st.error(f"ChromaDB Error: {e}")
                            chroma_success = False
                        
                        if minio_success and chroma_success:
                            st.success(f"Deleted {selected_file_name}")
                            st.rerun()
                        else:
                            st.error("Failed to delete file.")
        else:
            st.info("No files found in storage.")

    st.divider()
    
    # Advanced Options Expander
    with st.expander("⚙️ Advanced Options", expanded=False):
        if st.button("Clear Dashboard", width="stretch"):
            st.session_state.df = None
            st.session_state.messages = []
            # Clear specific report keys
            keys_to_clear = [
                "spend_report", "risk_report", "supplier_report", 
                "contract_report", "po_report", "compliance_report", 
                "exec_summary_report"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.divider()
    
    # Run All Analysis Button
    if st.session_state.df is not None:
        if st.button("🚀 Run All Analysis", type="primary"):
            import concurrent.futures
            import time
            
            start_time = time.time()
            with st.spinner("Running comprehensive analysis..."):
                # Initialize Agents
                agents = {
                    "spend": SpendAnalysisAgent(),
                    "risk": RiskMonitoringAgent(),
                    "supplier": SupplierIntelligenceAgent(),
                    "contract": ContractIntelligenceAgent(),
                    "po": POAutomationAgent(),
                    "compliance": CompliancePolicyAgent()
                }
                
                # Define tasks with their specific queries
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

                # Execute in parallel (Reduced to 2 workers for stability)
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
                        status_text.text(f"Completed {completed_count}/{total_tasks} analyses... (Finished: {key.title()})")

                # Store results in session state
                st.session_state.spend_report = results["spend"]
                st.session_state.risk_report = results["risk"]
                st.session_state.supplier_report = results["supplier"]
                st.session_state.contract_report = results["contract"]
                st.session_state.po_report = results["po"]
                st.session_state.compliance_report = results["compliance"]
                
                # Generate Executive Summary from Spend and Risk insights
                st.session_state.exec_summary_report = f"### Financial Overview\n{st.session_state.spend_report}\n\n### Risk Overview\n{st.session_state.risk_report}"
                
                end_time = time.time()
                duration = end_time - start_time
                hours, rem = divmod(duration, 3600)
                minutes, seconds = divmod(rem, 60)
                time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                
                status_text.empty()
                progress_bar.empty()
                st.success("All analyses completed successfully!")
                print(f"Total Analysis Time: {time_str}")

# Main Content
st.title(" Procurement Assistant ")

if st.session_state.df is not None:
    tabs = st.tabs([
        "Executive Summary", "Dashboard", "Supplier Intelligence", 
        "Spend Analysis", "Risk & Alerts", "PO Insights", 
        "Contract Intelligence", "Compliance & Policy"
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
    st.info("Please upload a CSV file to get started.")

# Chatbot Interface (Persistent at bottom)
@st.fragment
def render_chat_interface():
    st.divider()
    st.subheader("💬 AI Assistant")

    # Container for chat history and new messages
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your procurement data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    class GeneralAssistant(BaseDeepAgent):
                        def __init__(self):
                            super().__init__("General Assistant", "Helpful assistant for procurement queries.")
                        
                        def run(self, query: str) -> str:
                            # Load project context from README.md
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
