import streamlit as st
import pandas as pd
import plotly.express as px
from backend.agents import (
    SupplierIntelligenceAgent, SpendAnalysisAgent, RiskMonitoringAgent,
    ContractIntelligenceAgent, POAutomationAgent, CompliancePolicyAgent
)

def render_executive_summary(df):
    st.header("Executive Summary")
    
    # Project Overview
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="color: #31333F; margin-top: 0;">🚀 Project Overview: Procurement Assistant AI</h4>
        <p style="color: #555;">
            The <strong>Procurement Assistant AI</strong> is an intelligent platform designed to automate and enhance procurement operations. 
            It integrates <strong>Multi-Agent AI Systems</strong> with <strong>Retrieval-Augmented Generation (RAG)</strong> to transform raw data into strategic intelligence.
        </p>
        <p style="color: #555; margin-bottom: 0;">
            <strong>Functional Capabilities:</strong>
            <br>• <strong>🤖 Multi-Agent Architecture:</strong> Deploys specialized agents (Spend, Risk, Supplier, Contract) that run in parallel to analyze data from multiple dimensions simultaneously.
            <br>• <strong>🧠 RAG & LLM Integration:</strong> Combines a local Vector Database (ChromaDB) with Large Language Models to answer complex natural language queries about your procurement data.
            <br>• <strong>⚡ Automated Data Processing:</strong> Streamlines the ingestion, cleaning, and structuring of raw CSV files for immediate analysis.
            <br>• <strong>🛡️ Proactive Risk Management:</strong> Continuously monitors supplier reliability and compliance to mitigate supply chain disruptions before they occur.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Custom CSS for KPI Cards
    st.markdown("""
    <style>
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
        height: 100%;
    }
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .kpi-label {
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        color: #333;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .risk-high { color: #dc3545; }
    .risk-medium { color: #ffc107; }
    .risk-low { color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

    # Metrics Row with styling
    st.subheader("📊 Key Performance Indicators")
    
    avg_risk = df['SupplierRiskLevel'].mode()[0] if not df.empty else "N/A"
    risk_class = ""
    if avg_risk == "High": risk_class = "risk-high"
    elif avg_risk == "Medium": risk_class = "risk-medium"
    elif avg_risk == "Low": risk_class = "risk-low"

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">${df['TotalAmount'].sum():,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🏢</div>
            <div class="kpi-label">Active Suppliers</div>
            <div class="kpi-value">{df['SupplierID'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📝</div>
            <div class="kpi-label">Total POs</div>
            <div class="kpi-value">{df['POID'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Avg Risk Level</div>
            <div class="kpi-value {risk_class}">{avg_risk}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    st.subheader("AI Insights")
    
    if "exec_summary_report" not in st.session_state:
        st.session_state.exec_summary_report = None

    btn_label = "Regenerate Executive Briefing" if st.session_state.exec_summary_report else "Generate Executive Briefing"
    if st.button(btn_label):
        with st.spinner("Analyzing data..."):
            spend_agent = SpendAnalysisAgent()
            risk_agent = RiskMonitoringAgent()
            
            spend_insight = spend_agent.run("Summarize key spend highlights for executives.")
            risk_insight = risk_agent.run("Highlight critical risks for executives.")
            
            report = f"### Financial Overview\n{spend_insight}\n\n### Risk Overview\n{risk_insight}"
            st.session_state.exec_summary_report = report
    
    if st.session_state.exec_summary_report:
        st.markdown(st.session_state.exec_summary_report)

def render_dashboard(df):
    st.header("Procurement Dashboard")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">📊 Dashboard Overview</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Visualizes high-level procurement metrics. Use the filters below to customize the view.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Interactive Filters ---
    with st.expander("🔍 Filter Data", expanded=True):
        col_f1, col_f2 = st.columns(2)
        
        filtered_df = df.copy()
        
        with col_f1:
            if 'ItemCategory' in df.columns:
                categories = ["All"] + sorted(df['ItemCategory'].unique().tolist())
                selected_category = st.selectbox("Select Category", categories)
                if selected_category != "All":
                    filtered_df = filtered_df[filtered_df['ItemCategory'] == selected_category]
        
        with col_f2:
            if 'PODate' in df.columns:
                # Ensure datetimes are valid
                df['PODate'] = pd.to_datetime(df['PODate'])
                filtered_df['PODate'] = pd.to_datetime(filtered_df['PODate'])
                
                min_date = df['PODate'].min().date()
                max_date = df['PODate'].max().date()
                
                date_range = st.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_df = filtered_df[(filtered_df['PODate'].dt.date >= start_date) & (filtered_df['PODate'].dt.date <= end_date)]

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spend by Category")
        if 'ItemCategory' in filtered_df.columns and not filtered_df.empty:
            fig = px.pie(filtered_df, values='TotalAmount', names='ItemCategory', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
            
    with col2:
        st.subheader("Spend Trend")
        if 'PODate' in filtered_df.columns and not filtered_df.empty:
            monthly_spend = filtered_df.groupby(filtered_df['PODate'].dt.to_period('M'))['TotalAmount'].sum().reset_index()
            monthly_spend['PODate'] = monthly_spend['PODate'].astype(str)
            fig = px.area(monthly_spend, x='PODate', y='TotalAmount', markers=True, line_shape='spline')
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), xaxis_title="Month", yaxis_title="Spend ($)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")

    st.subheader("Top Suppliers by Spend")
    if not filtered_df.empty:
        top_suppliers = filtered_df.groupby('SupplierName')['TotalAmount'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_suppliers, x='SupplierName', y='TotalAmount', color='TotalAmount', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_title="Supplier", yaxis_title="Total Spend ($)")
        st.plotly_chart(fig, use_container_width=True)

def render_supplier_intelligence(df):
    st.header("Supplier Intelligence")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">🏢 Supplier Intelligence</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            AI-driven analysis of supplier performance. The matrix below correlates Delivery vs. Quality.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Supplier Performance Matrix ---
    st.subheader("🎯 Supplier Performance Matrix")
    if 'OnTimeDelivery%' in df.columns and 'QualityScore' in df.columns:
        # Aggregate data per supplier
        supplier_metrics = df.groupby('SupplierName').agg({
            'OnTimeDelivery%': 'mean',
            'QualityScore': 'mean',
            'TotalAmount': 'sum',
            'SupplierRiskLevel': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
        }).reset_index()
        
        fig = px.scatter(
            supplier_metrics, 
            x='OnTimeDelivery%', 
            y='QualityScore', 
            size='TotalAmount', 
            color='SupplierRiskLevel',
            hover_name='SupplierName',
            color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'},
            size_max=60,
            title="Delivery vs. Quality (Size = Spend)"
        )
        # Add quadrants
        fig.add_hline(y=supplier_metrics['QualityScore'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Quality")
        fig.add_vline(x=supplier_metrics['OnTimeDelivery%'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Delivery")
        
        st.plotly_chart(fig, use_container_width=True)

    agent = SupplierIntelligenceAgent()
    
    if "supplier_report" not in st.session_state:
        st.session_state.supplier_report = None

    btn_label = "Re-analyze Suppliers" if st.session_state.supplier_report else "Analyze Suppliers"
    if st.button(btn_label):
        with st.spinner("Running Supplier Intelligence Agent..."):
            insight = agent.run("Provide a detailed analysis of top suppliers and their performance.")
            st.session_state.supplier_report = insight
            
    if st.session_state.supplier_report:
        st.info(st.session_state.supplier_report)
            
    display_df = df[['SupplierName', 'SupplierRating', 'OnTimeDelivery%', 'QualityScore']].drop_duplicates().reset_index(drop=True)
    display_df.index = display_df.index + 1
    st.dataframe(display_df, use_container_width=True)

def render_spend_analysis(df):
    st.header("Spend Analysis")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">💰 Spend Analysis</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Deep dive into financial data to identify spending patterns, detect anomalies, and uncover cost-saving opportunities across categories.
        </p>
    </div>
    """, unsafe_allow_html=True)
    agent = SpendAnalysisAgent()
    
    if "spend_report" not in st.session_state:
        st.session_state.spend_report = None

    btn_label = "Re-analyze Spend" if st.session_state.spend_report else "Analyze Spend"
    if st.button(btn_label):
        with st.spinner("Running Spend Analysis Agent..."):
            insight = agent.run("Analyze spend patterns, identifying anomalies and opportunities.")
            st.session_state.spend_report = insight

    if st.session_state.spend_report:
        st.write(st.session_state.spend_report)

def render_risk_monitoring(df):
    st.header("Risk Monitoring")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">⚠️ Risk & Alerts</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Proactive monitoring of supply chain risks, highlighting high-risk suppliers and potential disruptions to ensure business continuity.
        </p>
    </div>
    """, unsafe_allow_html=True)
    agent = RiskMonitoringAgent()
    
    if "risk_report" not in st.session_state:
        st.session_state.risk_report = None

    btn_label = "Re-analyze Risks" if st.session_state.risk_report else "Analyze Risks"
    if st.button(btn_label):
        with st.spinner("Running Risk Monitoring Agent..."):
            insight = agent.run("Identify high-risk suppliers and potential supply chain disruptions.")
            st.session_state.risk_report = insight
            
    if st.session_state.risk_report:
        st.write(st.session_state.risk_report)
            
    st.subheader("High Risk Suppliers")
    if 'SupplierRiskLevel' in df.columns:
        high_risk = df[df['SupplierRiskLevel'] == 'High']
        st.dataframe(high_risk)

def render_contract_intelligence(df):
    st.header("Contract Intelligence")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">📜 Contract Intelligence</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Automated review of contract terms to track expirations, renewal dates, and compliance with agreed-upon service levels.
        </p>
    </div>
    """, unsafe_allow_html=True)
    agent = ContractIntelligenceAgent()
    
    if "contract_report" not in st.session_state:
        st.session_state.contract_report = None

    btn_label = "Re-analyze Contracts" if st.session_state.contract_report else "Analyze Contracts"
    if st.button(btn_label):
        with st.spinner("Running Contract Intelligence Agent..."):
            insight = agent.run("Review contracts for expiry and compliance risks.")
            st.session_state.contract_report = insight
            
    if st.session_state.contract_report:
        st.write(st.session_state.contract_report)

def render_po_automation(df):
    st.header("PO Automation")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">📝 Purchase Order Insights</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Analyzes Purchase Order lifecycles to detect processing delays, price discrepancies, and efficiency bottlenecks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    agent = POAutomationAgent()
    
    if "po_report" not in st.session_state:
        st.session_state.po_report = None

    btn_label = "Re-analyze POs" if st.session_state.po_report else "Analyze POs"
    if st.button(btn_label):
        with st.spinner("Running PO Automation Agent..."):
            insight = agent.run("Analyze Purchase Orders for delays and price discrepancies.")
            st.session_state.po_report = insight
            
    if st.session_state.po_report:
        st.write(st.session_state.po_report)

def render_compliance_policy(df):
    st.header("Compliance & Policy")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h5 style="color: #31333F; margin-top: 0;">🛡️ Compliance & Policy</h5>
        <p style="color: #555; margin-bottom: 0; font-size: 0.9rem;">
            Audits procurement activities against internal policies and budget constraints to ensure regulatory adherence and prevent maverick spending.
        </p>
    </div>
    """, unsafe_allow_html=True)
    agent = CompliancePolicyAgent()
    
    if "compliance_report" not in st.session_state:
        st.session_state.compliance_report = None

    btn_label = "Re-check Compliance" if st.session_state.compliance_report else "Check Compliance"
    if st.button(btn_label):
        with st.spinner("Running Compliance Agent..."):
            insight = agent.run("Check for policy violations and budget adherence.")
            st.session_state.compliance_report = insight
            
    if st.session_state.compliance_report:
        st.write(st.session_state.compliance_report)
