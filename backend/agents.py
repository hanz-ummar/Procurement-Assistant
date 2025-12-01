from typing import List, Dict, Any
from llama_index.core import VectorStoreIndex, PromptTemplate
from loguru import logger
from .database import get_vector_store
from .llm import init_llm

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        # Ensure LLM is initialized
        init_llm()

    def run(self, input_data: Any) -> str:
        raise NotImplementedError("Agents must implement the run method")

class RAGRetrievalAgent(Agent):
    """
    Wrapper for direct retrieval if needed (debugging/testing).
    """
    def __init__(self):
        super().__init__("RAGRetrievalAgent", "Retrieves relevant information from the knowledge base.")
        vector_store, _ = get_vector_store()
        self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    def run(self, query: str, n_results: int = 5) -> List[str]:
        """
        Retrieves top-k relevant document chunks for a given query.
        """
        retriever = self.index.as_retriever(similarity_top_k=n_results)
        nodes = retriever.retrieve(query)
        return [node.get_content() for node in nodes]

class BaseDeepAgent(Agent):
    def __init__(self, name: str, role: str):
        super().__init__(name, role)
        vector_store, _ = get_vector_store()
        self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    def _generate_insight(self, query: str, prompt_template_str: str) -> str:
        """
        Uses LlamaIndex Query Engine with a custom prompt to generate insights.
        """
        # Adapt prompt to LlamaIndex format (requires {context_str} and {query_str})
        # We replace user's {context} with {context_str} and {query} with {query_str}
        llama_prompt_str = prompt_template_str.replace("{context}", "{context_str}").replace("{query}", "{query_str}")
        
        # Add system role to the prompt
        system_msg = f"You are the {self.name}. {self.role}\n"
        full_prompt_str = system_msg + llama_prompt_str
from typing import List, Dict, Any
from llama_index.core import VectorStoreIndex, PromptTemplate
from loguru import logger
from .database import get_vector_store
from .llm import init_llm

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        # Ensure LLM is initialized
        init_llm()

    def run(self, input_data: Any) -> str:
        raise NotImplementedError("Agents must implement the run method")

class RAGRetrievalAgent(Agent):
    """
    Wrapper for direct retrieval if needed (debugging/testing).
    """
    def __init__(self):
        super().__init__("RAGRetrievalAgent", "Retrieves relevant information from the knowledge base.")
        self.index = get_index()

    def run(self, query: str, n_results: int = 5) -> List[str]:
        """
        Retrieves top-k relevant document chunks for a given query.
        """
        retriever = self.index.as_retriever(similarity_top_k=n_results)
        nodes = retriever.retrieve(query)
        return [node.get_content() for node in nodes]

_index_cache = None

def get_index():
    """
    Returns the cached VectorStoreIndex to avoid repeated initialization overhead.
    """
    global _index_cache
    if _index_cache:
        return _index_cache
    
    import time
    start_time = time.time()
    logger.info("Loading VectorStoreIndex...")
    vector_store, _ = get_vector_store()
    _index_cache = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    logger.info(f"VectorStoreIndex loaded in {time.time() - start_time:.2f}s")
    return _index_cache

class BaseDeepAgent(Agent):
    def __init__(self, name: str, role: str):
        super().__init__(name, role)
        self.index = get_index()

    def _generate_insight(self, query: str, prompt_template_str: str) -> str:
        """
        Uses LlamaIndex Query Engine with a custom prompt to generate insights.
        """
        # Adapt prompt to LlamaIndex format (requires {context_str} and {query_str})
        # We replace user's {context} with {context_str} and {query} with {query_str}
        llama_prompt_str = prompt_template_str.replace("{context}", "{context_str}").replace("{query}", "{query_str}")
        
        # Add system role to the prompt
        system_msg = f"You are the {self.name}. {self.role}\n"
        full_prompt_str = system_msg + llama_prompt_str
        
        qa_template = PromptTemplate(full_prompt_str)
        
        # Configure Query Engine
        query_engine = self.index.as_query_engine(
            text_qa_template=qa_template,
            similarity_top_k=4,
            response_mode="compact"
        )
        
        logger.info(f"Agent {self.name} starting query: {query}")
        import time
        q_start = time.time()
        response = query_engine.query(query)
        q_duration = time.time() - q_start
        logger.info(f"Agent {self.name} query finished in {q_duration:.2f}s")
        
        logger.info(f"Agent {self.name} Response: {response}")
        if hasattr(response, 'source_nodes'):
            logger.info(f"Source Nodes: {len(response.source_nodes)}")
            for node in response.source_nodes:
                logger.debug(f"Node Score: {node.score}")
        
        return str(response)

# --- Functional Agents ---

class SupplierIntelligenceAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("Supplier Intelligence Agent", "Evaluates supplier performance and rankings.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "analyze supplier performance. Provide a ranking of top suppliers and detailed performance analysis (Delivery, Quality).\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)

class SpendAnalysisAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("Spend Analysis Agent", "Analyzes spend patterns and identifies cost-saving opportunities.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "analyze the spend data. Identify monthly/yearly trends, category-wise spend, and cost-saving opportunities.\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)

class RiskMonitoringAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("Risk Monitoring Agent", "Identifies supplier risks and supply chain disruptions.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "identify high-risk suppliers and potential supply chain disruptions.\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)

class ContractIntelligenceAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("Contract Intelligence Agent", "Reviews contracts for expiry, clauses, and compliance.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "review the contract details. Focus on Expiry dates, Key clauses, and Compliance status.\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)

class POAutomationAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("PO Automation Agent", "Automates PO creation and tracks delivery status.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "analyze the Purchase Order data. Identify potential issues with Delivery Tracking and Price Validation.\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)

class CompliancePolicyAgent(BaseDeepAgent):
    def __init__(self):
        super().__init__("Compliance & Policy Agent", "Ensures adherence to procurement policies and regulations.")

    def run(self, query: str) -> str:
        prompt_template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "check for Policy Violations, Budget Deviations, and Missing Documentation.\n"
            "Provide a concise summary with bullet points.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        return self._generate_insight(query, prompt_template)
