import sys
import logging
from typing import Optional
import pandas as pd

# Setup debug logging
logging.basicConfig(
    filename='mcp_server_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("Starting MCP Server...")
    from mcp.server.fastmcp import FastMCP
    from backend.database import MinioClient
    import chromadb
    from backend.config import Config
    import os

    # Initialize FastMCP Server
    logger.info("Initializing FastMCP...")
    mcp = FastMCP("Procurement Assistant")
    logger.info("FastMCP initialized successfully.")
except Exception as e:
    logger.exception("Failed to start MCP Server")
    sys.exit(1)

# ============================================================================
# Helper Functions
# ============================================================================

def get_minio_client():
    """Lazy initialization of MinIO client"""
    from backend.database import MinioClient
    return MinioClient()

def get_query_engine(similarity_top_k: int = 5):
    """Get LlamaIndex query engine with proper embeddings"""
    from llama_index.core import VectorStoreIndex
    from backend.database import get_vector_store
    from backend.llm import get_llm, get_embed_model
    
    vector_store, storage_context = get_vector_store()
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context,
        embed_model=get_embed_model()
    )
    return index.as_query_engine(llm=get_llm(), similarity_top_k=similarity_top_k)

def get_agent(agent_type: str):
    """Get a specific agent instance"""
    from backend.agents import (
        SpendAnalysisAgent, RiskMonitoringAgent, SupplierIntelligenceAgent,
        ContractIntelligenceAgent, POAutomationAgent, CompliancePolicyAgent
    )
    
    agents = {
        "spend": SpendAnalysisAgent,
        "risk": RiskMonitoringAgent,
        "supplier": SupplierIntelligenceAgent,
        "contract": ContractIntelligenceAgent,
        "po": POAutomationAgent,
        "compliance": CompliancePolicyAgent
    }
    
    if agent_type.lower() not in agents:
        raise ValueError(f"Unknown agent type: {agent_type}. Available: {list(agents.keys())}")
    
    return agents[agent_type.lower()]()

def get_procurement_dataframe(source_file: Optional[str] = None) -> pd.DataFrame:
    """
    Get procurement data as pandas DataFrame from MinIO.
    
    Behavior:
    - If source_file is provided, load exactly that file.
    - If no source_file:
        - If one file exists, load that.
        - If multiple files exist, raise an error asking to specify source_file.
    """
    import io

    minio_client = get_minio_client()
    files = minio_client.list_files()

    if not files:
        raise RuntimeError("No procurement files found in storage. Please upload a CSV file first.")

    # Determine which file to use
    if source_file:
        if source_file not in files:
            raise RuntimeError(f"File '{source_file}' not found. Available files: {', '.join(files)}")
        target_file = source_file
    else:
        if len(files) == 1:
            target_file = files[0]
        else:
            raise RuntimeError(
                "Multiple procurement files found. "
                "Please specify 'source_file' when calling this tool. "
                f"Available files: {', '.join(files)}"
            )

    content = minio_client.get_file_content(target_file)
    if not content:
        raise RuntimeError(f"Could not read content of '{target_file}'.")

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        logger.error(f"Error parsing CSV '{target_file}': {e}")
        raise RuntimeError(f"Failed to parse CSV file '{target_file}'.") from e

    return df

# ============================================================================
# MCP Tools - File Management
# ============================================================================

@mcp.tool()
def list_procurement_files() -> list[str]:
    """
    List all procurement files currently stored in the system (MinIO).
    Returns a list of filenames.
    """
    try:
        minio_client = get_minio_client()
        files = minio_client.list_files()
        return files if files else ["No files found"]
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return [f"Error listing files: {str(e)}"]

@mcp.tool()
def get_file_info(filename: str) -> str:
    """
    Get information about a specific procurement file.
    
    Args:
        filename: Name of the file to get information about
    """
    try:
        minio_client = get_minio_client()
        files = minio_client.list_files()
        
        if filename not in files:
            return f"File '{filename}' not found. Available files: {', '.join(files)}"
        
        # Get file content size
        content = minio_client.get_file_content(filename)
        if content:
            size_kb = len(content) / 1024
            return f"File: {filename}\nSize: {size_kb:.2f} KB\nStatus: Available"
        else:
            return f"File '{filename}' exists but could not be retrieved."
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return f"Error: {str(e)}"

# ============================================================================
# MCP Tools - Data Querying
# ============================================================================

@mcp.tool()
def query_procurement_data(query: str, n_results: int = 5) -> str:
    """
    Search the procurement knowledge base (ChromaDB) for relevant information.
    Use this to find specific details about suppliers, contracts, risks, or spend.
    
    Args:
        query: The search query (e.g., "high risk suppliers", "IT spend analysis")
        n_results: Number of results to return (default: 5)
    """
    try:
        query_engine = get_query_engine(similarity_top_k=n_results)
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        logger.error(f"Error querying data: {e}")
        return f"Error querying data: {str(e)}"

# ============================================================================
# MCP Tools - Agent-Based Analysis
# ============================================================================

@mcp.tool()
def analyze_spend(query: Optional[str] = None) -> str:
    """
    Run spend analysis using the Spend Analysis Agent.
    Analyzes spend patterns, identifies anomalies, and finds cost-saving opportunities.
    
    Args:
        query: Optional specific query. If not provided, runs general spend analysis.
    """
    try:
        agent = get_agent("spend")
        query = query or "Analyze spend patterns, identifying anomalies and opportunities."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in spend analysis: {e}")
        return f"Error running spend analysis: {str(e)}"

@mcp.tool()
def analyze_risk(query: Optional[str] = None) -> str:
    """
    Run risk analysis using the Risk Monitoring Agent.
    Identifies high-risk suppliers and potential supply chain disruptions.
    
    Args:
        query: Optional specific query. If not provided, runs general risk analysis.
    """
    try:
        agent = get_agent("risk")
        query = query or "Identify high-risk suppliers and potential supply chain disruptions."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in risk analysis: {e}")
        return f"Error running risk analysis: {str(e)}"

@mcp.tool()
def analyze_suppliers(query: Optional[str] = None) -> str:
    """
    Run supplier analysis using the Supplier Intelligence Agent.
    Provides detailed analysis of top suppliers and their performance.
    
    Args:
        query: Optional specific query. If not provided, runs general supplier analysis.
    """
    try:
        agent = get_agent("supplier")
        query = query or "Provide a detailed analysis of top suppliers and their performance."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in supplier analysis: {e}")
        return f"Error running supplier analysis: {str(e)}"

@mcp.tool()
def analyze_contracts(query: Optional[str] = None) -> str:
    """
    Run contract analysis using the Contract Intelligence Agent.
    Reviews contracts for expiry dates and compliance risks.
    
    Args:
        query: Optional specific query. If not provided, runs general contract analysis.
    """
    try:
        agent = get_agent("contract")
        query = query or "Review contracts for expiry and compliance risks."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in contract analysis: {e}")
        return f"Error running contract analysis: {str(e)}"

@mcp.tool()
def analyze_purchase_orders(query: Optional[str] = None) -> str:
    """
    Run PO analysis using the PO Automation Agent.
    Analyzes Purchase Orders for delays and price discrepancies.
    
    Args:
        query: Optional specific query. If not provided, runs general PO analysis.
    """
    try:
        agent = get_agent("po")
        query = query or "Analyze Purchase Orders for delays and price discrepancies."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in PO analysis: {e}")
        return f"Error running PO analysis: {str(e)}"

@mcp.tool()
def analyze_compliance(query: Optional[str] = None) -> str:
    """
    Run compliance analysis using the Compliance & Policy Agent.
    Checks for policy violations and budget adherence.
    
    Args:
        query: Optional specific query. If not provided, runs general compliance analysis.
    """
    try:
        agent = get_agent("compliance")
        query = query or "Check for policy violations and budget adherence."
        result = agent.run(query)
        return result
    except Exception as e:
        logger.error(f"Error in compliance analysis: {e}")
        return f"Error running compliance analysis: {str(e)}"

@mcp.tool()
def run_comprehensive_analysis() -> str:
    """
    Run all agent analyses in parallel and return a comprehensive report.
    This combines insights from all 6 specialized agents.
    """
    try:
        import concurrent.futures
        
        agents_config = {
            "spend": ("Analyze spend patterns, identifying anomalies and opportunities.", "spend"),
            "risk": ("Identify high-risk suppliers and potential supply chain disruptions.", "risk"),
            "supplier": ("Provide a detailed analysis of top suppliers and their performance.", "supplier"),
            "contract": ("Review contracts for expiry and compliance risks.", "contract"),
            "po": ("Analyze Purchase Orders for delays and price discrepancies.", "po"),
            "compliance": ("Check for policy violations and budget adherence.", "compliance")
        }
        
        results = {}
        
        def run_agent(key, query, agent_type):
            try:
                agent = get_agent(agent_type)
                return key, agent.run(query)
            except Exception as e:
                logger.error(f"Error in {key} analysis: {e}")
                return key, f"Error: {str(e)}"
        
        # Run agents in parallel (max 2 workers to avoid overload)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(run_agent, key, query, agent_type): key
                for key, (query, agent_type) in agents_config.items()
            }
            
            for future in concurrent.futures.as_completed(futures):
                key, result = future.result()
                results[key] = result
        
        # Format comprehensive report
        report = "# Comprehensive Procurement Analysis Report\n\n"
        report += "## Executive Summary\n\n"
        report += f"**Spend Analysis:**\n{results.get('spend', 'N/A')[:200]}...\n\n"
        report += f"**Risk Overview:**\n{results.get('risk', 'N/A')[:200]}...\n\n"
        report += "\n## Detailed Analysis\n\n"
        
        for key, result in results.items():
            report += f"### {key.title()} Analysis\n{result}\n\n"
        
        return report
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        return f"Error running comprehensive analysis: {str(e)}"

@mcp.tool()
def compare_suppliers(supplier1: str, supplier2: str, source_file: Optional[str] = None) -> str:
    """
    Compare two suppliers side-by-side on key metrics: delivery performance, quality, cost, and risk.
    
    Args:
        supplier1: Name of the first supplier to compare
        supplier2: Name of the second supplier to compare
        source_file: Optional specific CSV filename to use. If omitted and multiple
                     files exist, an error will be returned asking to specify it.
    """
    try:
        df = get_procurement_dataframe(source_file=source_file)
        
        # Filter data for both suppliers
        supplier1_data = df[df['SupplierName'].str.contains(supplier1, case=False, na=False)]
        supplier2_data = df[df['SupplierName'].str.contains(supplier2, case=False, na=False)]
        
        if supplier1_data.empty:
            return f"Error: Supplier '{supplier1}' not found in the data."
        if supplier2_data.empty:
            return f"Error: Supplier '{supplier2}' not found in the data."
        
        # Calculate metrics for supplier 1
        s1_metrics = {
            'name': supplier1_data['SupplierName'].iloc[0],
            'avg_delivery': supplier1_data['OnTimeDelivery%'].mean() if 'OnTimeDelivery%' in supplier1_data.columns else 0,
            'avg_quality': supplier1_data['QualityScore'].mean() if 'QualityScore' in supplier1_data.columns else 0,
            'total_spend': supplier1_data['TotalAmount'].sum() if 'TotalAmount' in supplier1_data.columns else 0,
            'avg_price': supplier1_data['UnitPrice'].mean() if 'UnitPrice' in supplier1_data.columns else 0,
            'risk_level': supplier1_data['SupplierRiskLevel'].mode()[0] if 'SupplierRiskLevel' in supplier1_data.columns and not supplier1_data['SupplierRiskLevel'].mode().empty else 'Unknown',
            'order_count': len(supplier1_data),
            'compliance': supplier1_data['ComplianceStatus'].mode()[0] if 'ComplianceStatus' in supplier1_data.columns and not supplier1_data['ComplianceStatus'].mode().empty else 'Unknown'
        }
        
        # Calculate metrics for supplier 2
        s2_metrics = {
            'name': supplier2_data['SupplierName'].iloc[0],
            'avg_delivery': supplier2_data['OnTimeDelivery%'].mean() if 'OnTimeDelivery%' in supplier2_data.columns else 0,
            'avg_quality': supplier2_data['QualityScore'].mean() if 'QualityScore' in supplier2_data.columns else 0,
            'total_spend': supplier2_data['TotalAmount'].sum() if 'TotalAmount' in supplier2_data.columns else 0,
            'avg_price': supplier2_data['UnitPrice'].mean() if 'UnitPrice' in supplier2_data.columns else 0,
            'risk_level': supplier2_data['SupplierRiskLevel'].mode()[0] if 'SupplierRiskLevel' in supplier2_data.columns and not supplier2_data['SupplierRiskLevel'].mode().empty else 'Unknown',
            'order_count': len(supplier2_data),
            'compliance': supplier2_data['ComplianceStatus'].mode()[0] if 'ComplianceStatus' in supplier2_data.columns and not supplier2_data['ComplianceStatus'].mode().empty else 'Unknown'
        }
        
        # Generate comparison report
        report = f"# Supplier Comparison: {s1_metrics['name']} vs {s2_metrics['name']}\n\n"
        report += "## Performance Metrics\n\n"
        report += f"| Metric | {s1_metrics['name']} | {s2_metrics['name']} | Winner |\n"
        report += "|--------|" + "-" * (len(s1_metrics['name']) + 2) + "|" + "-" * (len(s2_metrics['name']) + 2) + "|--------|\n"
        
        # Delivery Performance
        s1_del = s1_metrics['avg_delivery']
        s2_del = s2_metrics['avg_delivery']
        winner_del = s1_metrics['name'] if s1_del > s2_del else s2_metrics['name'] if s2_del > s1_del else "Tie"
        report += f"| **Delivery %** | {s1_del:.2f}% | {s2_del:.2f}% | {winner_del} |\n"
        
        # Quality Score
        s1_qual = s1_metrics['avg_quality']
        s2_qual = s2_metrics['avg_quality']
        winner_qual = s1_metrics['name'] if s1_qual > s2_qual else s2_metrics['name'] if s2_qual > s1_qual else "Tie"
        report += f"| **Quality Score** | {s1_qual:.2f} | {s2_qual:.2f} | {winner_qual} |\n"
        
        # Total Spend
        s1_spend = s1_metrics['total_spend']
        s2_spend = s2_metrics['total_spend']
        report += f"| **Total Spend** | ${s1_spend:,.2f} | ${s2_spend:,.2f} | - |\n"
        
        # Average Price
        s1_price = s1_metrics['avg_price']
        s2_price = s2_metrics['avg_price']
        winner_price = s2_metrics['name'] if s2_price < s1_price else s1_metrics['name'] if s1_price < s2_price else "Tie"
        report += f"| **Avg Unit Price** | ${s1_price:.2f} | ${s2_price:.2f} | {winner_price} (lower is better) |\n"
        
        # Risk Level
        report += f"| **Risk Level** | {s1_metrics['risk_level']} | {s2_metrics['risk_level']} | - |\n"
        
        # Order Count
        report += f"| **Order Count** | {s1_metrics['order_count']} | {s2_metrics['order_count']} | - |\n"
        
        # Compliance
        report += f"| **Compliance** | {s1_metrics['compliance']} | {s2_metrics['compliance']} | - |\n"
        
        report += "\n## Summary\n\n"
        
        # Determine overall winner
        wins_s1 = 0
        wins_s2 = 0
        
        if s1_del > s2_del: wins_s1 += 1
        elif s2_del > s1_del: wins_s2 += 1
        
        if s1_qual > s2_qual: wins_s1 += 1
        elif s2_qual > s1_qual: wins_s2 += 1
        
        if s2_price < s1_price: wins_s2 += 1
        elif s1_price < s2_price: wins_s1 += 1
        
        if wins_s1 > wins_s2:
            report += f"**Overall Winner: {s1_metrics['name']}** ({wins_s1} metrics better)\n"
        elif wins_s2 > wins_s1:
            report += f"**Overall Winner: {s2_metrics['name']}** ({wins_s2} metrics better)\n"
        else:
            report += "**Tie** - Both suppliers perform similarly\n"
        
        report += f"\n**Recommendation:** "
        if s1_metrics['risk_level'] == 'Low' and s2_metrics['risk_level'] != 'Low':
            report += f"Consider {s1_metrics['name']} for lower risk."
        elif s2_metrics['risk_level'] == 'Low' and s1_metrics['risk_level'] != 'Low':
            report += f"Consider {s2_metrics['name']} for lower risk."
        elif s1_del > s2_del and s1_qual > s2_qual:
            report += f"Consider {s1_metrics['name']} for better delivery and quality."
        elif s2_del > s1_del and s2_qual > s1_qual:
            report += f"Consider {s2_metrics['name']} for better delivery and quality."
        else:
            report += "Evaluate based on specific requirements and priorities."
        
        return report
    except Exception as e:
        logger.error(f"Error comparing suppliers: {e}")
        return f"Error comparing suppliers: {str(e)}"

@mcp.tool()
def get_expiring_contracts(days_ahead: int = 90, source_file: Optional[str] = None) -> str:
    """
    Find contracts that are expiring within the specified number of days.
    
    Args:
        days_ahead: Number of days to look ahead (default: 90)
        source_file: Optional specific CSV filename to use. If omitted and multiple
                     files exist, an error will be returned asking to specify it.
    """
    try:
        from datetime import datetime, timedelta
        
        df = get_procurement_dataframe(source_file=source_file)
        
        if 'ContractEndDate' not in df.columns:
            return "Error: Contract end dates not available in the data."
        
        # Calculate cutoff date
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        # Parse contract end dates
        expiring_contracts = []
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.get('ContractEndDate')):
                    continue
                
                # Try different date formats
                end_date = None
                date_str = str(row['ContractEndDate'])
                
                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                    try:
                        end_date = datetime.strptime(date_str.split()[0], fmt)
                        break
                    except:
                        continue
                
                if end_date and end_date <= cutoff_date:
                    expiring_contracts.append({
                        'contract_id': row.get('ContractID', 'N/A'),
                        'supplier': row.get('SupplierName', 'N/A'),
                        'end_date': end_date.strftime('%Y-%m-%d'),
                        'days_until_expiry': (end_date - datetime.now()).days,
                        'risk_level': row.get('SupplierRiskLevel', 'Unknown'),
                        'total_amount': row.get('TotalAmount', 0)
                    })
            except Exception as e:
                logger.debug(f"Error parsing contract date: {e}")
                continue
        
        if not expiring_contracts:
            return f"No contracts expiring in the next {days_ahead} days."
        
        # Remove duplicates and sort by expiry date
        unique_contracts = {}
        for contract in expiring_contracts:
            key = contract['contract_id']
            if key not in unique_contracts or contract['days_until_expiry'] < unique_contracts[key]['days_until_expiry']:
                unique_contracts[key] = contract
        
        sorted_contracts = sorted(unique_contracts.values(), key=lambda x: x['days_until_expiry'])
        
        # Generate report
        report = f"# Contracts Expiring in Next {days_ahead} Days\n\n"
        report += f"**Total Contracts Found:** {len(sorted_contracts)}\n\n"
        report += "| Contract ID | Supplier | Expiry Date | Days Left | Risk Level |\n"
        report += "|-------------|----------|-------------|-----------|------------|\n"
        
        urgent_count = 0
        for contract in sorted_contracts:
            days_left = contract['days_until_expiry']
            if days_left <= 30:
                urgent_count += 1
                report += f"| **{contract['contract_id']}** | **{contract['supplier']}** | **{contract['end_date']}** | **{days_left}** ⚠️ | **{contract['risk_level']}** |\n"
            else:
                report += f"| {contract['contract_id']} | {contract['supplier']} | {contract['end_date']} | {days_left} | {contract['risk_level']} |\n"
        
        if urgent_count > 0:
            report += f"\n⚠️ **{urgent_count} contract(s) expiring within 30 days - URGENT ACTION REQUIRED**\n"
        
        report += "\n## Recommendations\n\n"
        report += "1. Initiate contract renewal discussions for urgent contracts\n"
        report += "2. Review supplier performance before renewing\n"
        report += "3. Consider alternative suppliers for high-risk contracts\n"
        report += "4. Plan for contract transition if not renewing\n"
        
        return report
    except Exception as e:
        logger.error(f"Error getting expiring contracts: {e}")
        return f"Error getting expiring contracts: {str(e)}"

@mcp.tool()
def export_report(report_type: str, format: str = "excel", source_file: Optional[str] = None) -> str:
    """
    Export analysis reports to Excel or CSV format.
    
    Args:
        report_type: Type of report to export (spend, risk, supplier, contract, po, compliance, comprehensive)
        format: Export format - 'excel' or 'csv' (default: excel)
        source_file: Optional specific CSV filename to use. If omitted and multiple
                     files exist, an error will be returned asking to specify it.
    """
    try:
        import pandas as pd
        from datetime import datetime
        import os
        
        # Validate report type
        valid_types = ['spend', 'risk', 'supplier', 'contract', 'po', 'compliance', 'comprehensive']
        if report_type.lower() not in valid_types:
            return f"Error: Invalid report type. Available: {', '.join(valid_types)}"
        
        # Get data
        df = get_procurement_dataframe(source_file=source_file)
        
        # Generate report data based on type
        export_df = None
        filename = None
        
        if report_type.lower() == 'spend':
            if 'ItemCategory' in df.columns and 'TotalAmount' in df.columns:
                export_df = df.groupby('ItemCategory').agg({
                    'TotalAmount': 'sum',
                    'UnitPrice': 'mean',
                    'POID': 'count'
                }).reset_index()
                export_df.columns = ['Category', 'Total Spend', 'Avg Price', 'Order Count']
                filename = f"spend_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif report_type.lower() == 'supplier':
            if 'SupplierName' in df.columns:
                export_df = df.groupby('SupplierName').agg({
                    'OnTimeDelivery%': 'mean' if 'OnTimeDelivery%' in df.columns else 'first',
                    'QualityScore': 'mean' if 'QualityScore' in df.columns else 'first',
                    'TotalAmount': 'sum',
                    'SupplierRiskLevel': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
                }).reset_index()
                export_df.columns = ['Supplier', 'Avg Delivery %', 'Avg Quality', 'Total Spend', 'Risk Level']
                filename = f"supplier_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif report_type.lower() == 'contract':
            if 'ContractID' in df.columns:
                contract_cols = ['ContractID', 'SupplierName', 'ContractEndDate', 'SupplierRiskLevel', 'TotalAmount']
                available_cols = [col for col in contract_cols if col in df.columns]
                export_df = df[available_cols].drop_duplicates(subset=['ContractID'] if 'ContractID' in df.columns else None)
                filename = f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif report_type.lower() == 'comprehensive':
            # Create a comprehensive report with multiple sheets (Excel only)
            if format.lower() != 'excel':
                return "Error: Comprehensive reports are only available in Excel format (multiple sheets)."
            
            filename = f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filepath = os.path.join(os.getcwd(), f"{filename}.xlsx")
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Spend Summary
                if 'ItemCategory' in df.columns:
                    spend_df = df.groupby('ItemCategory')['TotalAmount'].sum().reset_index()
                    spend_df.columns = ['Category', 'Total Spend']
                    spend_df.to_excel(writer, sheet_name='Spend Summary', index=False)
                
                # Supplier Performance
                if 'SupplierName' in df.columns:
                    supplier_cols = ['SupplierName']
                    if 'OnTimeDelivery%' in df.columns: supplier_cols.append('OnTimeDelivery%')
                    if 'QualityScore' in df.columns: supplier_cols.append('QualityScore')
                    if 'TotalAmount' in df.columns: supplier_cols.append('TotalAmount')
                    if 'SupplierRiskLevel' in df.columns: supplier_cols.append('SupplierRiskLevel')
                    
                    supplier_df = df[supplier_cols].groupby('SupplierName').agg({
                        col: 'mean' if col in ['OnTimeDelivery%', 'QualityScore'] else 'sum' if col == 'TotalAmount' else lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
                        for col in supplier_cols if col != 'SupplierName'
                    }).reset_index()
                    supplier_df.to_excel(writer, sheet_name='Supplier Performance', index=False)
                
                # Contracts
                if 'ContractID' in df.columns:
                    contract_cols = ['ContractID', 'SupplierName', 'ContractEndDate', 'SupplierRiskLevel']
                    available_contract_cols = [col for col in contract_cols if col in df.columns]
                    contract_df = df[available_contract_cols].drop_duplicates(subset=['ContractID'])
                    contract_df.to_excel(writer, sheet_name='Contracts', index=False)
            
            return f"✅ Comprehensive report exported to: {filepath}\n\nContains multiple sheets: Spend Summary, Supplier Performance, Contracts"
        
        else:
            # For other report types, export filtered data
            export_df = df.copy()
            filename = f"{report_type}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if export_df is None or export_df.empty:
            return f"Error: Could not generate {report_type} report. Required columns may be missing."
        
        # Export based on format
        if format.lower() == 'excel':
            filepath = os.path.join(os.getcwd(), f"{filename}.xlsx")
            export_df.to_excel(filepath, index=False, engine='openpyxl')
            return f"✅ Report exported to Excel: {filepath}\n\nRows: {len(export_df)}, Columns: {len(export_df.columns)}"
        
        elif format.lower() == 'csv':
            filepath = os.path.join(os.getcwd(), f"{filename}.csv")
            export_df.to_csv(filepath, index=False)
            return f"✅ Report exported to CSV: {filepath}\n\nRows: {len(export_df)}, Columns: {len(export_df.columns)}"
        
        else:
            return f"Error: Invalid format '{format}'. Use 'excel' or 'csv'."
    
    except ImportError:
        return "Error: openpyxl library required for Excel export. Install with: pip install openpyxl"
    except Exception as e:
        logger.error(f"Error exporting report: {e}")
        return f"Error exporting report: {str(e)}"

# ============================================================================
# MCP Resources - Expose Procurement Data
# ============================================================================

@mcp.resource("procurement://files")
def list_files_resource() -> list[dict]:
    """Resource listing all procurement files"""
    try:
        minio_client = get_minio_client()
        files = minio_client.list_files()
        return [
            {
                "uri": f"procurement://file/{file}",
                "name": file,
                "description": f"Procurement data file: {file}",
                "mimeType": "text/csv"
            }
            for file in files
        ]
    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        return []

@mcp.resource("procurement://file/{filename}")
def get_file_resource(filename: str) -> str:
    """Get content of a specific procurement file"""
    try:
        minio_client = get_minio_client()
        content = minio_client.get_file_content(filename)
        if content:
            # Try to decode as text (CSV)
            try:
                return content.decode('utf-8')
            except:
                return f"Binary file content (size: {len(content)} bytes)"
        else:
            return f"File '{filename}' not found or could not be retrieved."
    except Exception as e:
        logger.error(f"Error getting file resource: {e}")
        return f"Error: {str(e)}"

# ============================================================================
# MCP Prompts - Predefined Queries
# ============================================================================

@mcp.prompt()
def prompt_spend_analysis() -> str:
    """
    Prompt template for spend analysis.
    Use this to analyze procurement spend patterns and identify cost-saving opportunities.
    """
    return """Analyze the procurement spend data and provide insights on:
1. Monthly and yearly spending trends
2. Category-wise spend distribution
3. Top spending areas
4. Cost-saving opportunities
5. Anomalies or unusual patterns

Please provide a comprehensive analysis with specific recommendations."""

@mcp.prompt()
def prompt_risk_assessment() -> str:
    """
    Prompt template for risk assessment.
    Use this to identify high-risk suppliers and potential supply chain disruptions.
    """
    return """Conduct a comprehensive risk assessment of the procurement data:
1. Identify high-risk suppliers based on delivery performance, quality issues, or financial stability
2. Flag potential supply chain disruptions
3. Assess contract compliance risks
4. Highlight areas requiring immediate attention
5. Provide risk mitigation recommendations

Please prioritize risks by severity and urgency."""

@mcp.prompt()
def prompt_supplier_performance() -> str:
    """
    Prompt template for supplier performance evaluation.
    Use this to rank and evaluate supplier performance.
    """
    return """Evaluate supplier performance and provide:
1. Top 10 suppliers ranked by overall performance
2. Delivery performance metrics (on-time delivery rate)
3. Quality performance metrics
4. Cost competitiveness analysis
5. Recommendations for supplier relationship management

Include specific metrics and actionable insights for each supplier."""

@mcp.prompt()
def prompt_contract_review() -> str:
    """
    Prompt template for contract review.
    Use this to review contracts for expiry dates and compliance.
    """
    return """Review all contracts in the procurement data:
1. List contracts expiring in the next 90 days
2. Identify contracts with compliance risks
3. Highlight key contract terms and clauses
4. Assess contract value and renewal recommendations
5. Flag any missing or incomplete contract information

Provide a prioritized list of contracts requiring attention."""

@mcp.prompt()
def prompt_compliance_check() -> str:
    """
    Prompt template for compliance and policy check.
    Use this to check for policy violations and budget adherence.
    """
    return """Perform a comprehensive compliance and policy check:
1. Identify policy violations
2. Check budget adherence and deviations
3. Flag missing documentation
4. Assess regulatory compliance
5. Provide recommendations for remediation

Prioritize findings by severity and include specific examples."""

@mcp.prompt()
def prompt_executive_summary() -> str:
    """
    Prompt template for executive summary.
    Use this to generate a high-level executive summary of procurement status.
    """
    return """Generate an executive summary of the procurement data covering:
1. Overall spend overview (total, trends, key categories)
2. Top risks and concerns
3. Supplier performance highlights
4. Key contracts and renewals
5. Compliance status
6. Top 3 recommendations for action

Keep it concise (under 500 words) and focused on actionable insights for leadership."""

if __name__ == "__main__":
    try:
        print("Starting MCP server...", file=sys.stderr)
        logger.info("Calling mcp.run()...")
        mcp.run()
    except Exception as e:
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        logger.exception("Fatal error in mcp.run()")
        sys.exit(1)
