"""
Pytest configuration and shared fixtures for all tests.
"""
import pytest
import pandas as pd
import io
from pathlib import Path

# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_csv_data():
    """Sample CSV data with valid procurement records"""
    return b"""SupplierName,PONumber,PODate,DeliveryDate,Amount,Category,Status
Acme Corporation,PO-001,2024-01-15,2024-01-20,15000,IT,Completed
Beta Industries,PO-002,2024-01-16,2024-01-25,8500,HR,Completed
Gamma Solutions,PO-003,2024-01-17,2024-02-01,22000,IT,Pending
Delta Services,PO-004,2024-01-18,2024-01-22,5000,Facilities,Completed
Epsilon Tech,PO-005,2024-01-19,2024-02-10,12000,IT,Delayed
Zeta Supplies,PO-006,2024-01-20,2024-01-23,3500,Office,Completed
Acme Corporation,PO-007,2024-02-01,2024-02-05,18000,IT,Completed
Beta Industries,PO-008,2024-02-02,2024-02-15,9000,HR,Pending
Gamma Solutions,PO-009,2024-02-03,2024-03-01,25000,IT,Delayed
Delta Services,PO-010,2024-02-04,2024-02-08,4500,Facilities,Completed"""


@pytest.fixture
def sample_dataframe(sample_csv_data):
    """Sample DataFrame parsed from CSV data"""
    return pd.read_csv(io.BytesIO(sample_csv_data))


@pytest.fixture
def invalid_csv_data():
    """CSV data missing required columns"""
    return b"""Name,Date,Price
Test,2024-01-01,100"""


@pytest.fixture
def large_csv_data():
    """Generate larger CSV for performance testing"""
    rows = [
        "SupplierName,PONumber,PODate,DeliveryDate,Amount,Category,Status"
    ]
    
    suppliers = ["Acme Corp", "Beta Inc", "Gamma LLC", "Delta Co", "Epsilon Ltd"]
    categories = ["IT", "HR", "Facilities", "Office", "Marketing"]
    statuses = ["Completed", "Pending", "Delayed"]
    
    for i in range(100):
        supplier = suppliers[i % len(suppliers)]
        category = categories[i % len(categories)]
        status = statuses[i % len(statuses)]
        row = f"{supplier},PO-{i:04d},2024-01-{(i%28)+1:02d},2024-02-{(i%28)+1:02d},{1000+i*100},{category},{status}"
        rows.append(row)
    
    return "\n".join(rows).encode()


# ============================================================================
# Service Fixtures (MinIO, ChromaDB)
# ============================================================================

@pytest.fixture(scope="session")
def minio_client():
    """
    MinIO client for integration tests.
    Assumes MinIO is running via docker-compose.
    """
    from backend.database import MinioClient
    
    client = MinioClient()
    yield client
    
    # Cleanup: Remove all test files after session
    try:
        files = client.list_files()
        for file in files:
            if file.startswith("test_"):
                client.delete_file(file)
    except Exception:
        pass


@pytest.fixture(scope="session")
def vector_store():
    """
    ChromaDB vector store for integration tests.
    Assumes ChromaDB is running via docker-compose.
    """
    from backend.database import get_vector_store
    
    vector_store, storage_context = get_vector_store()
    yield vector_store
    
    # Note: We keep test data in ChromaDB for now
    # In production, use a separate test collection


@pytest.fixture(scope="function")
def clean_test_file(minio_client):
    """
    Context manager for test files - ensures cleanup after each test.
    
    Usage:
        def test_something(clean_test_file):
            filename = clean_test_file("test_data.csv")
            # ... test code ...
            # File automatically deleted after test
    """
    test_files = []
    
    def create_test_file(filename):
        test_files.append(filename)
        return filename
    
    yield create_test_file
    
    # Cleanup
    for filename in test_files:
        try:
            minio_client.delete_file(filename)
        except Exception:
            pass


# ============================================================================
# LLM/Agent Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def llm_initialized():
    """
    Ensure LLM is initialized once per test session.
    Skips tests if Ollama is not available.
    """
    from backend.llm import init_llm
    import requests
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            pytest.skip("Ollama not available")
    except Exception:
        pytest.skip("Ollama not running at localhost:11434")
    
    # Initialize LLM
    try:
        init_llm()
    except Exception as e:
        pytest.skip(f"Failed to initialize LLM: {e}")
    
    return True


@pytest.fixture
def mock_llm_response():
    """
    Mock LLM response for testing without actual LLM calls.
    Useful for fast unit tests.
    """
    class MockLLM:
        def complete(self, prompt):
            class Response:
                text = "This is a mocked LLM response for testing purposes."
            return Response()
        
        def query(self, prompt):
            return self.complete(prompt)
    
    return MockLLM()


# ============================================================================
# Test Data Paths
# ============================================================================

@pytest.fixture
def test_data_dir():
    """Path to test data directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def golden_dataset_path(test_data_dir):
    """Path to golden dataset for AI quality testing"""
    path = test_data_dir / "golden_procurement.csv"
    if not path.exists():
        pytest.skip(f"Golden dataset not found at {path}")
    return path


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Print test configuration info"""
    print("\n" + "="*70)
    print("🧪 Procurement Assistant Test Suite")
    print("="*70)
    print("Running tests with current hybrid setup:")
    print("  ✓ ChromaDB: Docker (localhost:8000)")
    print("  ✓ MinIO: Docker (localhost:9000)")
    print("  ✓ Ollama: Host (localhost:11434)")
    print("  ✓ Streamlit: Host")
    print("="*70 + "\n")


def pytest_collection_modifyitems(config, items):
    """
    Auto-mark tests based on their location and requirements.
    """
    for item in items:
        # Mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark AI tests
        if "test_ai" in item.name or "ai" in str(item.fspath):
            item.add_marker(pytest.mark.ai)
            item.add_marker(pytest.mark.slow)
        
        # Mark tests that use LLM
        if "llm" in item.name or "agent" in item.name:
            item.add_marker(pytest.mark.slow)
