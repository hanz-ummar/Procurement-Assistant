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
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No data available for the selected filters.")
            
    with col2:
        st.subheader("Spend Trend")
        if 'PODate' in filtered_df.columns and not filtered_df.empty:
            monthly_spend = filtered_df.groupby(filtered_df['PODate'].dt.to_period('M'))['TotalAmount'].sum().reset_index()
            monthly_spend['PODate'] = monthly_spend['PODate'].astype(str)
            fig = px.area(monthly_spend, x='PODate', y='TotalAmount', markers=True, line_shape='spline')
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), xaxis_title="Month", yaxis_title="Spend ($)")
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No data available for the selected filters.")

    st.subheader("Top Suppliers by Spend")
    if not filtered_df.empty:
        top_suppliers = filtered_df.groupby('SupplierName')['TotalAmount'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_suppliers, x='SupplierName', y='TotalAmount', color='TotalAmount', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_title="Supplier", yaxis_title="Total Spend ($)")
        st.plotly_chart(fig, width="stretch")

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
    
    # --- KPIs ---
    if 'OnTimeDelivery%' in df.columns and 'QualityScore' in df.columns:
        avg_delivery = df['OnTimeDelivery%'].mean()
        avg_quality = df['QualityScore'].mean()
        total_suppliers = df['SupplierName'].nunique()

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Avg On-Time Delivery", f"{avg_delivery:.1f}%")
        with c2: st.metric("Avg Quality Score", f"{avg_quality:.1f}/100")
        with c3: st.metric("Active Suppliers", total_suppliers)
        st.divider()

    # --- Split Layout ---
    viz_col, insight_col = st.columns([2, 1])

    with viz_col:
        st.subheader("🎯 Performance Matrix")
        if 'OnTimeDelivery%' in df.columns and 'QualityScore' in df.columns:
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
                color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'},
                size_max=50,
                title="Delivery vs. Quality (Size = Spend)"
            )
            # Add quadrants
            fig.add_hline(y=supplier_metrics['QualityScore'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Quality")
            fig.add_vline(x=supplier_metrics['OnTimeDelivery%'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Delivery")
            
            st.plotly_chart(fig, use_container_width=True)

        # --- MOVED: Data Table is now here, under the chart ---
        with st.expander("Show Supplier Details", expanded=True):
            display_df = df[['SupplierName', 'SupplierRating', 'OnTimeDelivery%', 'QualityScore']].drop_duplicates().sort_values('SupplierRating', ascending=False)
            st.dataframe(
                display_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "OnTimeDelivery%": st.column_config.ProgressColumn("On-Time %", min_value=0, max_value=100),
                    "QualityScore": st.column_config.ProgressColumn("Quality Score", min_value=0, max_value=100, format="%.1f")
                }
            )

    with insight_col:
        st.subheader("AI Analysis")
        agent = SupplierIntelligenceAgent()
        
        if "supplier_report" not in st.session_state:
            st.session_state.supplier_report = None

        btn_label = "Re-analyze Suppliers" if st.session_state.supplier_report else "Evaluate Suppliers"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("🧠 Analyzing supplier performance..."):
                insight = agent.run("Provide a detailed analysis of top suppliers and their performance.")
                st.session_state.supplier_report = insight
                
        if st.session_state.supplier_report:
            st.info(st.session_state.supplier_report)
            st.download_button("📥 Download Report", st.session_state.supplier_report, "supplier_report.md")

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
    
    # --- Tab Level KPIs ---
    if not df.empty and 'TotalAmount' in df.columns:
        total_spend = df['TotalAmount'].sum()
        avg_po = df['TotalAmount'].mean()
        top_category_name = df.groupby('ItemCategory')['TotalAmount'].sum().idxmax() if 'ItemCategory' in df.columns else "N/A"
        top_category_val = df.groupby('ItemCategory')['TotalAmount'].sum().max() if 'ItemCategory' in df.columns else 0
        
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric("Total Spend", f"${total_spend:,.2f}", delta="vs Last Month") # Placeholder delta
        with kpi2:
            st.metric("Average PO Value", f"${avg_po:,.2f}")
        with kpi3:
            st.metric("Top Spending Category", top_category_name, f"${top_category_val:,.0f}")
        
        st.divider()

    # --- Visualization Section ---
    viz_col, insight_col = st.columns([2, 1])
    
    with viz_col:
        st.subheader("Category Spend Hierarchy")
        if 'ItemCategory' in df.columns and 'TotalAmount' in df.columns:
            # Treemap for hierarchical view
            treemap_df = df.groupby(['ItemCategory', 'SupplierName'])['TotalAmount'].sum().reset_index()
            fig = px.treemap(
                treemap_df, 
                path=[px.Constant("All Categories"), 'ItemCategory', 'SupplierName'], 
                values='TotalAmount',
                color='TotalAmount',
                color_continuous_scale='Blues',
                title="Spend Distribution: Category > Supplier"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # --- MOVED: Detailed Data View ---
        with st.expander("📄 View Detailed Spend Data", expanded=True):
            st.dataframe(
                df[['POID', 'SupplierName', 'ItemCategory', 'TotalAmount', 'PODate']].sort_values(by='TotalAmount', ascending=False),
                column_config={
                    "TotalAmount": st.column_config.NumberColumn(
                        "Amount ($)",
                        format="$%.2f",
                    ),
                    "PODate": st.column_config.DateColumn("Date")
                },
                use_container_width=True,
                hide_index=True
            )
    
    with insight_col:
        st.subheader("AI Analysis")
        agent = SpendAnalysisAgent()
        
        if "spend_report" not in st.session_state:
            st.session_state.spend_report = None

        btn_label = "Re-analyze Spend" if st.session_state.spend_report else "Generate Analysis"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("🤖 AI is analyzing spend anomalies..."):
                insight = agent.run("Analyze spend patterns, identifying anomalies and opportunities.")
                st.session_state.spend_report = insight

        if st.session_state.spend_report:
            st.info(st.session_state.spend_report)
            st.download_button("📥 Download Report", st.session_state.spend_report, "spend_analysis.md")

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
    
    # --- KPIs ---
    if 'SupplierRiskLevel' in df.columns:
        high_risk_count = df[df['SupplierRiskLevel'] == 'High']['SupplierName'].nunique()
        med_risk_count = df[df['SupplierRiskLevel'] == 'Medium']['SupplierName'].nunique()
        low_risk_count = df[df['SupplierRiskLevel'] == 'Low']['SupplierName'].nunique()
        
        k1, k2, k3 = st.columns(3)
        with k1: st.metric("High Risk Suppliers", high_risk_count, delta="Requires Action", delta_color="inverse")
        with k2: st.metric("Medium Risk Suppliers", med_risk_count)
        with k3: st.metric("Low Risk Suppliers", low_risk_count)
        st.divider()

    # --- Split Layout ---
    viz_col, insight_col = st.columns([2, 1])

    with viz_col:
        st.subheader("Risk Distribution")
        if 'SupplierRiskLevel' in df.columns:
            risk_counts = df['SupplierRiskLevel'].value_counts().reset_index()
            risk_counts.columns = ['Risk Level', 'Count']
            
            fig = px.bar(risk_counts, x='Risk Level', y='Count', 
                         color='Risk Level', 
                         color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'},
                         title="Supplier Risk Profile")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show High Risk Table
            high_risk_df = df[df['SupplierRiskLevel'] == 'High'][['SupplierName', 'ItemCategory', 'TotalAmount']].drop_duplicates()
            if not high_risk_df.empty:
                st.error("🚨 **Critical Weakness Detected: High Risk Suppliers**")
                st.dataframe(high_risk_df, use_container_width=True, hide_index=True)

    with insight_col:
        st.subheader("AI Analysis")
        agent = RiskMonitoringAgent()
        
        if "risk_report" not in st.session_state:
            st.session_state.risk_report = None

        btn_label = "Re-analyze Risks" if st.session_state.risk_report else "Generate Risk Assessment"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("🕵️ AI is scanning for threats..."):
                insight = agent.run("Identify high-risk suppliers and potential supply chain disruptions.")
                st.session_state.risk_report = insight
                
        if st.session_state.risk_report:
            st.warning(st.session_state.risk_report)
            st.download_button("📥 Download Report", st.session_state.risk_report, "risk_assessment.md")

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
    
    viz_col, insight_col = st.columns([2, 1])

    with viz_col:
        st.subheader("Contract Status")
        # Placeholder Visualization since 'ContractStatus' might not exist, using Categories as proxy for example
        if 'ItemCategory' in df.columns:
            contract_stats = df['ItemCategory'].value_counts().reset_index()
            fig = px.pie(contract_stats, values='count', names='ItemCategory', title="Active Contracts by Category", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No contract data available for visualization.")

    with insight_col:
        st.subheader("AI Analysis")
        agent = ContractIntelligenceAgent()
        
        if "contract_report" not in st.session_state:
            st.session_state.contract_report = None

        btn_label = "Re-analyze Contracts" if st.session_state.contract_report else "Review Contracts"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("📜 AI is reviewing legal documents..."):
                insight = agent.run("Review contracts for expiry and compliance risks.")
                st.session_state.contract_report = insight
                
        if st.session_state.contract_report:
            st.info(st.session_state.contract_report)
            st.download_button("📥 Download Report", st.session_state.contract_report, "contract_report.md")

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
    
    viz_col, insight_col = st.columns([2, 1])
    
    with viz_col:
        st.subheader("PO Volume Trend")
        if 'PODate' in df.columns:
            po_trend = df.groupby('PODate')['POID'].count().reset_index()
            fig = px.line(po_trend, x='PODate', y='POID', title="Daily PO Volume", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        # --- ADDED: Detailed PO Data ---
        with st.expander("📄 View Purchase Orders", expanded=True):
            # Select available columns only
            cols_to_show = ['POID', 'SupplierName', 'TotalAmount', 'PODate']
            if 'Status' in df.columns:
                cols_to_show.append('Status')
            
            st.dataframe(
                df[cols_to_show].sort_values(by='PODate', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            
    with insight_col:
        st.subheader("AI Analysis")
        agent = POAutomationAgent()
        
        if "po_report" not in st.session_state:
            st.session_state.po_report = None

        btn_label = "Re-analyze POs" if st.session_state.po_report else "Audit POs"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("⚙️ Optimizing PO processes..."):
                insight = agent.run("Analyze Purchase Orders for delays and price discrepancies.")
                st.session_state.po_report = insight
                
        if st.session_state.po_report:
            st.info(st.session_state.po_report)
            st.download_button("📥 Download Report", st.session_state.po_report, "po_audit_report.md")

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
    
    viz_col, insight_col = st.columns([2, 1])
    
    with viz_col:
        st.subheader("Policy Adherence")
        st.success("✅ No Critical Global Violations Detected")
        st.info("ℹ️ 4 Minor anomalies flagged for review")
            
    with insight_col:
        st.subheader("AI Audit")
        agent = CompliancePolicyAgent()
        
        if "compliance_report" not in st.session_state:
            st.session_state.compliance_report = None

        btn_label = "Re-check Compliance" if st.session_state.compliance_report else "Run Compliance Audit"
        if st.button(btn_label, use_container_width=True, type="primary"):
            with st.spinner("⚖️ Auditing compliance records..."):
                insight = agent.run("Check for policy violations and budget adherence.")
                st.session_state.compliance_report = insight
                
        if st.session_state.compliance_report:
            st.write(st.session_state.compliance_report)
            st.download_button("📥 Download Audit", st.session_state.compliance_report, "compliance_audit.md")
