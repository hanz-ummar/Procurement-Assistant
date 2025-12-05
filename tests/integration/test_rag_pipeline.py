"""
Integration tests for RAG pipeline.
Tests end-to-end: CSV upload → Embedding → Retrieval → Query
Requires: MinIO, ChromaDB, and Ollama running
"""
import pytest
import io
from backend.database import MinioClient
from backend.ingestion import DataPreprocessingAgent
from backend.agents import RAGRetrievalAgent, SpendAnalysisAgent


@pytest.mark.integration
@pytest.mark.slow
class TestRAGPipeline:
    """Test complete RAG pipeline"""
    
    def test_ingest_and_retrieve(self, minio_client, clean_test_file, sample_csv_data, llm_initialized):
        """Test full pipeline: Upload CSV → Process → Embed → Retrieve"""
        filename = clean_test_file("test_rag_pipeline.csv")
        
        # Step 1: Upload CSV to MinIO
        minio_client.upload_file(filename, io.BytesIO(sample_csv_data), len(sample_csv_data))
        
        # Step 2: Process and ingest
        agent = DataPreprocessingAgent()
        success, message = agent.process_csv(sample_csv_data, filename)
        
        # Should succeed
        assert success == True, f"Ingestion failed: {message}"
        
        # Step 3: Query the data
        rag_agent = RAGRetrievalAgent()
        results = rag_agent.run("List all suppliers", n_results=5)
        
        # Should return results
        assert results is not None
        assert len(results) > 0
    
    @pytest.mark.slow
    def test_semantic_search_quality(self, sample_csv_data, clean_test_file, minio_client, llm_initialized):
        """Test that semantic search returns relevant results"""
        filename = clean_test_file("test_semantic_search.csv")
        
        # Ingest data
        minio_client.upload_file(filename, io.BytesIO(sample_csv_data), len(sample_csv_data))
        agent = DataPreprocessingAgent()
        success, _ = agent.process_csv(sample_csv_data, filename)
        assert success
        
        # Query for IT-related items
        rag_agent = RAGRetrievalAgent()
        results = rag_agent.run("IT spending and technology purchases", n_results=3)
        
        # Results should contain IT-related terms
        results_str = str(results).lower()
        assert any(keyword in results_str for keyword in ['it', 'tech', 'acme', 'gamma', 'epsilon'])


@pytest.mark.integration
@pytest.mark.slow
class TestAgentWithRAG:
    """Test agents using RAG retrieval"""
    
    def test_spend_agent_uses_rag(self, sample_csv_data, clean_test_file, minio_client, llm_initialized):
        """Test SpendAnalysisAgent retrieves and analyzes data"""
        filename = clean_test_file("test_spend_agent.csv")
        
        # Ingest data
        minio_client.upload_file(filename, io.BytesIO(sample_csv_data), len(sample_csv_data))
        agent_ingest = DataPreprocessingAgent()
        success, _ = agent_ingest.process_csv(sample_csv_data, filename)
        assert success
        
        # Run spend analysis
        spend_agent = SpendAnalysisAgent()
        report = spend_agent.run("What is the total spend by category?")
        
        # Should return a non-empty report
        assert report is not None
        assert len(report) > 50, "Report should have substantial content"
        
        # Should mention categories or spending
        report_lower = report.lower()
        assert any(keyword in report_lower for keyword in [
            'spend', 'cost', 'amount', 'category', 'it', 'hr', 'total'
        ])
    
    @pytest.mark.slow
    def test_multiple_agents_concurrent(self, sample_csv_data, clean_test_file, minio_client, llm_initialized):
        """Test multiple agents can query simultaneously"""
        import concurrent.futures
        
        filename = clean_test_file("test_concurrent.csv")
        
        # Ingest data
        minio_client.upload_file(filename, io.BytesIO(sample_csv_data), len(sample_csv_data))
        agent_ingest = DataPreprocessingAgent()
        success, _ = agent_ingest.process_csv(sample_csv_data, filename)
        assert success
        
        # Run multiple agents in parallel
        from backend.agents import RiskMonitoringAgent, SupplierIntelligenceAgent
        
        agents = [
            SpendAnalysisAgent(),
            RiskMonitoringAgent(),
            SupplierIntelligenceAgent()
        ]
        
        queries = [
            "Analyze spending trends",
            "Identify risks",
            "Rank suppliers"
        ]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(agent.run, query) for agent, query in zip(agents, queries)]
            results = [f.result() for f in futures]
        
        # All should succeed
        assert all(len(r) > 0 for r in results)
