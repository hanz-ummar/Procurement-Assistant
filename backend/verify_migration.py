import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.llm import init_llm
from backend.database import get_vector_store
from backend.agents import SupplierIntelligenceAgent
from loguru import logger

def verify():
    logger.info("Starting Verification...")
    
    # 1. Test LLM Init
    try:
        init_llm()
        logger.info("✅ LLM Initialized")
    except Exception as e:
        logger.error(f"❌ LLM Init Failed: {e}")
        return

    # 2. Test Vector Store
    try:
        get_vector_store()
        logger.info("✅ Vector Store Initialized")
    except Exception as e:
        logger.error(f"❌ Vector Store Init Failed: {e}")
        return

    # 3. Test Agent Instantiation
    try:
        agent = SupplierIntelligenceAgent()
        logger.info(f"✅ Agent '{agent.name}' Instantiated")
    except Exception as e:
        logger.error(f"❌ Agent Instantiation Failed: {e}")
        return

    logger.info("🎉 Migration Verification Successful!")

if __name__ == "__main__":
    verify()
