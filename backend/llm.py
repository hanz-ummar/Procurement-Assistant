from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from loguru import logger
from .config import Config

_is_initialized = False

def init_llm():
    """
    Configures the global LlamaIndex Settings with Ollama models.
    Ensures initialization happens only once.
    """
    global _is_initialized
    if _is_initialized:
        return

    try:
        logger.info(f"Initializing LlamaIndex with LLM={Config.LLM_MODEL} and Embed={Config.EMBEDDING_MODEL}")
        
        Settings.llm = Ollama(
            model=Config.LLM_MODEL, 
            base_url=Config.OLLAMA_BASE_URL,
            request_timeout=300.0,
            additional_kwargs={"num_ctx": 4096}
        )
        
        Settings.embed_model = OllamaEmbedding(
            model_name=Config.EMBEDDING_MODEL,
            base_url=Config.OLLAMA_BASE_URL
        )
        
        _is_initialized = True
        logger.info("LlamaIndex Settings configured successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize LlamaIndex: {e}")
        raise e

def get_llm():
    """Get the configured LLM instance"""
    init_llm()
    return Settings.llm

def get_embed_model():
    """Get the configured embedding model instance"""
    init_llm()
    return Settings.embed_model
