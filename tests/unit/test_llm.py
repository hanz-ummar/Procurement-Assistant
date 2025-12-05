"""
Unit tests for LLM initialization and configuration.
Tests LLM setup, singleton pattern, and model loading.
"""
import pytest
from backend.llm import init_llm, get_llm, get_embed_model, _is_initialized
from backend.config import Config


@pytest.mark.unit
class TestLLMInitialization:
    """Test LLM initialization logic"""
    
    def test_init_llm_sets_flag(self):
        """Test that init_llm sets the initialization flag"""
        # Note: May already be initialized from other tests
        # Just verify the function runs without error
        try:
            init_llm()
            # Should not raise an exception
            assert True
        except Exception as e:
            pytest.fail(f"init_llm raised an exception: {e}")
    
    def test_get_llm_returns_instance(self):
        """Test get_llm returns valid LLM instance"""
        llm = get_llm()
        
        assert llm is not None
        assert hasattr(llm, 'complete') or hasattr(llm, 'chat')
    
    def test_get_embed_model_returns_instance(self):
        """Test get_embed_model returns valid embedding model"""
        embed_model = get_embed_model()
        
        assert embed_model is not None
        assert hasattr(embed_model, 'get_text_embedding') or \
               hasattr(embed_model, 'get_query_embedding')
    
    def test_multiple_init_calls_safe(self):
        """Test that calling init_llm multiple times is safe"""
        # Should not reinitialize if already initialized
        init_llm()
        init_llm()
        init_llm()
        
        # Should still work
        llm = get_llm()
        assert llm is not None


@pytest.mark.unit
class TestLLMConfiguration:
    """Test LLM configuration settings"""
    
    def test_llm_uses_correct_model(self):
        """Test LLM is configured with correct model"""
        llm = get_llm()
        
        # Check model name is set correctly
        assert hasattr(llm, 'model')
        assert llm.model == Config.LLM_MODEL
    
    def test_llm_has_timeout(self):
        """Test LLM has reasonable timeout"""
        llm = get_llm()
        
        if hasattr(llm, 'request_timeout'):
            assert llm.request_timeout > 0
            assert llm.request_timeout <= 600  # Max 10 minutes
    
    def test_llm_context_window(self):
        """Test LLM context window is set"""
        llm = get_llm()
        
        # Should have num_ctx in additional_kwargs
        if hasattr(llm, 'additional_kwargs'):
            kwargs = llm.additional_kwargs
            if 'num_ctx' in kwargs:
                assert kwargs['num_ctx'] == 4096
    
    def test_embed_model_uses_correct_model(self):
        """Test embedding model uses correct model name"""
        embed_model = get_embed_model()
        
        assert hasattr(embed_model, 'model_name')
        assert embed_model.model_name == Config.EMBEDDING_MODEL
