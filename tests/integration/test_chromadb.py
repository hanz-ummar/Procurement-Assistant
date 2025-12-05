"""
Integration tests for ChromaDB vector store.
Requires ChromaDB running via docker-compose.
"""
import pytest
from backend.database import get_vector_store


@pytest.mark.integration
class TestChromaDBConnection:
    """Test ChromaDB connection"""
    
    def test_chromadb_connection(self):
        """Test connection to ChromaDB"""
        vector_store, storage_context = get_vector_store()
        
        assert vector_store is not None
        assert storage_context is not None
    
    def test_vector_store_has_collection(self, vector_store):
        """Test vector store has associated collection"""
        assert vector_store is not None
        
        # Check it has chroma_collection attribute
        if hasattr(vector_store, 'chroma_collection'):
            assert vector_store.chroma_collection is not None


@pytest.mark.integration
class TestVectorStoreOperations:
    """Test vector store basic operations"""
    
    def test_vector_store_caching(self):
        """Test that vector store uses caching"""
        # Get vector store twice
        vs1, sc1 = get_vector_store()
        vs2, sc2 = get_vector_store()
        
        # Should return same instances (cached)
        assert vs1 is vs2
        assert sc1 is sc2
    
    @pytest.mark.slow
    def test_collection_persistence(self, vector_store):
        """Test that ChromaDB collection persists across connections"""
        # Get collection info
        if hasattr(vector_store, 'chroma_collection'):
            collection = vector_store.chroma_collection
            collection_name = collection.name
            
            # Reconnect
            vector_store2, _ = get_vector_store()
            collection2 = vector_store2.chroma_collection
            
            # Should be same collection
            assert collection2.name == collection_name
