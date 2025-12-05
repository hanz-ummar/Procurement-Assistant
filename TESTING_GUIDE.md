# Testing Guide

## 🧪 Test Suite Overview

This project includes a comprehensive test suite covering:
- **Unit Tests**: Fast tests for core logic (no external dependencies)
- **Integration Tests**: Tests with Docker services (MinIO, ChromaDB)
- **AI Tests**: Quality tests for LLM agent outputs
- **Coverage Target**: 60-70%

## 📋 Prerequisites

### Required Services
Before running tests, ensure these services are running:

```bash
# Start Docker services
docker-compose up -d

# Verify services are healthy
docker ps

# You should see:
# - procurement_minio (ports 9000, 9001)
# - procurement_chromadb (port 8000)
```

### Required: Ollama with Models
Ensure Ollama is running with required models:

```bash
# Check Ollama is running
ollama list

# Should show:
# - llama3.2:3b
# - bge-m3:567m

# If missing, pull them:
ollama pull llama3.2:3b
ollama pull bge-m3:567m
```

## 🚀 Running Tests

### Install Test Dependencies

```bash
# Using uv (recommended)
uv pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests

# Or using pip
pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests
```

### Run All Tests

```bash
# Run everything (takes ~2-5 minutes)
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=backend --cov-report=html
```

### Run Specific Test Categories

```bash
# Fast unit tests only (no Docker/Ollama needed for most)
pytest -m unit

# Integration tests (requires Docker services)
pytest -m integration

# AI quality tests (requires Ollama, slower)
pytest -m ai

# Skip slow tests
pytest -m "not slow"
```

### Run Specific Test Files

```bash
# Test configuration
pytest tests/unit/test_config.py -v

# Test MinIO integration
pytest tests/integration/test_minio.py -v

# Test agent quality
pytest tests/ai/test_agent_quality.py -v
```

### Run Specific Test Functions

```bash
# Run single test
pytest tests/unit/test_config.py::TestConfig::test_default_values -v

# Run all tests matching pattern
pytest -k "test_minio" -v
```

## 📊 Understanding Test Output

### Success Example
```
tests/unit/test_config.py::TestConfig::test_default_values PASSED [100%]

========== 1 passed in 0.05s ==========
```

### Failure Example
```
tests/unit/test_config.py::TestConfig::test_minio_endpoint_format FAILED
AssertionError: Endpoint should include port

========== 1 failed in 0.10s ==========
```

### Coverage Report
```
---------- coverage: platform win32, python 3.11.x -----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
backend/config.py                20      2    90%   15-16
backend/agents.py               120     25    79%   45-50, 88-92
backend/ingestion.py             85     30    65%   102-115
-----------------------------------------------------------
TOTAL                           250     60    76%
```

## 🎯 Test Markers

Tests are organized with markers for easy filtering:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (needs Docker)
- `@pytest.mark.ai` - AI/LLM tests (needs Ollama)
- `@pytest.mark.slow` - Tests taking > 5 seconds
- `@pytest.mark.e2e` - End-to-end tests (future)

## 🐛 Troubleshooting

### "No module named 'pytest'"
```bash
# Install pytest
pip install pytest pytest-cov
```

### "ChromaDB connection failed"
```bash
# Ensure Docker services are running
docker-compose up -d

# Check ChromaDB is accessible
curl http://localhost:8000/api/v1/heartbeat
```

### "Ollama not available"
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### "Tests are too slow"
```bash
# Skip slow AI tests during development
pytest -m "not slow" -v

# Run only fast unit tests
pytest tests/unit/ -v
```

### "MinIO tests failing"
```bash
# Reset MinIO container
docker-compose down
docker-compose up -d

# Clear test files manually
# Access MinIO console at http://localhost:9001
# Login: minioadmin / minioadmin
# Delete all files starting with "test_"
```

## 📈 Coverage Reports

### Generate HTML Coverage Report
```bash
pytest --cov=backend --cov-report=html

# Open in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

### Check Coverage Threshold
```bash
# Fail if coverage below 60%
pytest --cov=backend --cov-fail-under=60
```

## 🔄 Continuous Testing (Watch Mode)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw -- tests/unit/
```

## 📝 Writing New Tests

### Create a New Test File
```python
# tests/unit/test_example.py
import pytest

@pytest.mark.unit
def test_something():
    """Test description"""
    assert True
```

### Use Fixtures
```python
def test_with_sample_data(sample_csv_data):
    """Fixtures are defined in conftest.py"""
    assert len(sample_csv_data) > 0
```

### Mock External Services
```python
def test_without_ollama(mock_llm_response):
    """Use mock instead of real LLM"""
    response = mock_llm_response.complete("test")
    assert response.text is not None
```

## 🚀 CI/CD Integration (Future)

Tests will run automatically on:
- Every push to main branch
- Every pull request
- Nightly builds

See `.github/workflows/test.yml` (to be created)

## 📚 Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── __init__.py
├── unit/                    # Fast, isolated tests
│   ├── test_config.py      # Config validation
│   ├── test_llm.py         # LLM initialization
│   ├── test_ingestion.py   # CSV processing
│   └── test_agents.py      # Agent initialization
├── integration/             # Tests with Docker services
│   ├── test_minio.py       # MinIO operations
│   ├── test_chromadb.py    # Vector store
│   └── test_rag_pipeline.py # End-to-end RAG
└── ai/                      # AI quality tests
    └── test_agent_quality.py # Agent output validation
```

## ✅ Test Checklist for New Features

When adding new features, ensure you add:
- [ ] Unit tests for new functions
- [ ] Integration tests if using external services
- [ ] AI quality tests if adding new agents
- [ ] Update this documentation
- [ ] Tests pass locally before committing

## 🎓 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
