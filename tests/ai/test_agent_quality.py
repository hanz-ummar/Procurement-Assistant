"""
AI quality tests for agent outputs.
Tests that agents produce relevant, well-formatted responses.
"""
import pytest
from backend.agents import (
    SpendAnalysisAgent,
    RiskMonitoringAgent,
    SupplierIntelligenceAgent,
    ContractIntelligenceAgent,
    POAutomationAgent,
    CompliancePolicyAgent
)


@pytest.mark.ai
@pytest.mark.slow
class TestAgentOutputQuality:
    """Test that agent outputs meet quality standards"""
    
    def test_spend_agent_output_length(self, llm_initialized):
        """Test SpendAnalysisAgent produces adequate output"""
        agent = SpendAnalysisAgent()
        response = agent.run("Analyze overall spending patterns")
        
        # Should not be too short or too long
        assert len(response) > 100, "Response too brief"
        assert len(response) < 3000, "Response too verbose"
    
    def test_spend_agent_contains_keywords(self, llm_initialized):
        """Test SpendAnalysisAgent uses relevant terminology"""
        agent = SpendAnalysisAgent()
        response = agent.run("What are the top spending categories?")
        
        response_lower = response.lower()
        
        # Should mention spending-related terms
        relevant_keywords = ['spend', 'cost', 'amount', 'budget', 'category', 'total', 'supplier']
        matches = sum(1 for keyword in relevant_keywords if keyword in response_lower)
        
        assert matches >= 2, f"Response missing spending terminology. Found {matches} keywords."
    
    def test_risk_agent_identifies_risks(self, llm_initialized):
        """Test RiskMonitoringAgent mentions risk factors"""
        agent = RiskMonitoringAgent()
        response = agent.run("What are the main supply chain risks?")
        
        response_lower = response.lower()
        
        # Should mention risk-related concepts
        risk_keywords = ['risk', 'delay', 'late', 'failure', 'disruption', 'issue', 'concern']
        matches = sum(1 for keyword in risk_keywords if keyword in response_lower)
        
        assert matches >= 1, "Response should mention risk factors"
    
    def test_supplier_agent_ranks_suppliers(self, llm_initialized):
        """Test SupplierIntelligenceAgent provides rankings"""
        agent = SupplierIntelligenceAgent()
        response = agent.run("Rank top suppliers by performance")
        
        response_lower = response.lower()
        
        # Should mention suppliers and ranking concepts
        supplier_keywords = ['supplier', 'vendor', 'performance', 'top', 'rank', 'best', 'deliver']
        matches = sum(1 for keyword in supplier_keywords if keyword in response_lower)
        
        assert matches >= 2, "Response should rank suppliers"
    
    def test_agent_no_hallucination_markers(self, llm_initialized):
        """Test agents don't show common hallucination patterns"""
        agent = SpendAnalysisAgent()
        response = agent.run("Analyze procurement data")
        
        response_lower = response.lower()
        
        # Common hallucination phrases
        hallucination_markers = [
            "i don't have access",
            "i cannot access",
            "i don't have information",
            "as an ai",
            "i apologize",
            "i'm not able"
        ]
        
        for marker in hallucination_markers:
            assert marker not in response_lower, f"Found hallucination marker: {marker}"


@pytest.mark.ai
@pytest.mark.slow
class TestAgentStructuredOutput:
    """Test that agents produce well-structured outputs"""
    
    def test_output_has_sections(self, llm_initialized):
        """Test that longer outputs are organized into sections"""
        agent = SpendAnalysisAgent()
        response = agent.run("Provide comprehensive spend analysis")
        
        # Should have some structure (bullets, numbers, or headings)
        has_bullets = '•' in response or '-' in response
        has_numbers = any(f"{i}." in response for i in range(1, 6))
        has_headings = '##' in response or '**' in response
        
        assert has_bullets or has_numbers or has_headings, "Output should have structure"
    
    def test_output_not_truncated(self, llm_initialized):
        """Test outputs don't appear truncated"""
        agent = RiskMonitoringAgent()
        response = agent.run("Analyze all risk factors")
        
        # Should end properly (not mid-sentence)
        assert not response.endswith('...'), "Output appears truncated"
        assert len(response.split()) > 50, "Output seems incomplete"


@pytest.mark.ai
@pytest.mark.slow
class TestAgentConsistency:
    """Test agent output consistency"""
    
    def test_same_query_similar_length(self, llm_initialized):
        """Test repeated queries produce similar-length responses"""
        agent = SupplierIntelligenceAgent()
        query = "List top 3 suppliers"
        
        # Run twice
        response1 = agent.run(query)
        response2 = agent.run(query)
        
        len1, len2 = len(response1), len(response2)
        
        # Lengths should be within 50% of each other
        ratio = min(len1, len2) / max(len1, len2)
        assert ratio > 0.5, f"Response lengths vary too much: {len1} vs {len2}"
    
    def test_different_queries_different_content(self, llm_initialized):
        """Test different queries produce different responses"""
        agent = SpendAnalysisAgent()
        
        response1 = agent.run("What is total IT spending?")
        response2 = agent.run("What is total HR spending?")
        
        # Responses should differ
        assert response1 != response2
        
        # Should mention different categories
        assert 'it' in response1.lower() or 'hr' in response2.lower()


@pytest.mark.ai
@pytest.mark.slow
class TestAgentPerformance:
    """Test agent performance and speed"""
    
    def test_agent_responds_quickly(self, llm_initialized):
        """Test agents respond within reasonable time"""
        import time
        
        agent = CompliancePolicyAgent()
        
        start = time.time()
        response = agent.run("Check compliance status")
        duration = time.time() - start
        
        # Should complete in under 30 seconds
        assert duration < 30, f"Agent took {duration}s (too slow)"
        assert len(response) > 0
    
    def test_batch_queries_efficient(self, llm_initialized):
        """Test multiple queries don't cause exponential slowdown"""
        import time
        
        agent = POAutomationAgent()
        queries = [
            "Analyze PO delays",
            "Check PO discrepancies",
            "Review PO status"
        ]
        
        start = time.time()
        results = [agent.run(q) for q in queries]
        duration = time.time() - start
        
        # Should complete all in under 60 seconds
        assert duration < 60, f"Batch queries took {duration}s"
        assert all(len(r) > 0 for r in results)
