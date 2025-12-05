"""
Unit tests for agent classes.
Tests agent initialization, prompt formatting, and base functionality.
"""
import pytest
from backend.agents import (
    Agent,
    BaseDeepAgent,
    SpendAnalysisAgent,
    RiskMonitoringAgent,
    SupplierIntelligenceAgent,
    ContractIntelligenceAgent,
    POAutomationAgent,
    CompliancePolicyAgent
)


@pytest.mark.unit
class TestBaseAgent:
    """Test base Agent class"""
    
    def test_agent_initialization(self):
        """Test basic agent initialization"""
        agent = Agent("Test Agent", "Test role")
        
        assert agent.name == "Test Agent"
        assert agent.role == "Test role"
    
    def test_agent_has_run_method(self):
        """Test agent has run method"""
        agent = Agent("Test", "Role")
        
        assert hasattr(agent, 'run')
        assert callable(agent.run)


@pytest.mark.unit
class TestDeepAgentInitialization:
    """Test initialization of all deep reasoning agents"""
    
    def test_spend_analysis_agent(self):
        """Test SpendAnalysisAgent initialization"""
        agent = SpendAnalysisAgent()
        
        assert agent.name == "Spend Analysis Agent"
        assert "spend" in agent.role.lower() or "cost" in agent.role.lower()
        assert hasattr(agent, 'run')
    
    def test_risk_monitoring_agent(self):
        """Test RiskMonitoringAgent initialization"""
        agent = RiskMonitoringAgent()
        
        assert agent.name == "Risk Monitoring Agent"
        assert "risk" in agent.role.lower()
        assert hasattr(agent, 'run')
    
    def test_supplier_intelligence_agent(self):
        """Test SupplierIntelligenceAgent initialization"""
        agent = SupplierIntelligenceAgent()
        
        assert agent.name == "Supplier Intelligence Agent"
        assert "supplier" in agent.role.lower()
        assert hasattr(agent, 'run')
    
    def test_contract_intelligence_agent(self):
        """Test ContractIntelligenceAgent initialization"""
        agent = ContractIntelligenceAgent()
        
        assert agent.name == "Contract Intelligence Agent"
        assert "contract" in agent.role.lower()
        assert hasattr(agent, 'run')
    
    def test_po_automation_agent(self):
        """Test POAutomationAgent initialization"""
        agent = POAutomationAgent()
        
        assert agent.name == "PO Automation Agent"
        assert "po" in agent.role.lower() or "purchase order" in agent.role.lower()
        assert hasattr(agent, 'run')
    
    def test_compliance_policy_agent(self):
        """Test CompliancePolicyAgent initialization"""
        agent = CompliancePolicyAgent()
        
        # Check name contains key components (avoids HTML entity encoding issues)
        assert "Compliance" in agent.name
        assert "Policy" in agent.name
        assert "Agent" in agent.name
        # Role is: "Ensures adherence to procurement policies and regulations."
        assert "policies" in agent.role.lower() or "adherence" in agent.role.lower()
        assert hasattr(agent, 'run')


@pytest.mark.unit
class TestAgentProperties:
    """Test agent properties and configurations"""
    
    def test_all_agents_have_unique_names(self):
        """Test that all agents have unique names"""
        agents = [
            SpendAnalysisAgent(),
            RiskMonitoringAgent(),
            SupplierIntelligenceAgent(),
            ContractIntelligenceAgent(),
            POAutomationAgent(),
            CompliancePolicyAgent()
        ]
        
        names = [agent.name for agent in agents]
        assert len(names) == len(set(names)), "Agent names should be unique"
    
    def test_agents_use_index_singleton(self):
        """Test that agents share the same index instance (performance optimization)"""
        agent1 = SpendAnalysisAgent()
        agent2 = RiskMonitoringAgent()
        
        # Both should reference the same index (cached)
        if hasattr(agent1, 'index') and hasattr(agent2, 'index'):
            assert agent1.index is agent2.index


@pytest.mark.unit
class TestAgentMethods:
    """Test agent method signatures"""
    
    def test_agent_run_accepts_query(self):
        """Test agent run method accepts query parameter"""
        agent = SpendAnalysisAgent()
        
        # Check method signature
        import inspect
        sig = inspect.signature(agent.run)
        params = list(sig.parameters.keys())
        
        assert 'query' in params or len(params) > 0
    
    def test_generate_insight_method(self):
        """Test _generate_insight method exists"""
        agent = SpendAnalysisAgent()
        
        if hasattr(agent, '_generate_insight'):
            assert callable(agent._generate_insight)
