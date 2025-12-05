# 🧪 Quick Test Reference Card

## One-Line Commands

```bash
# Run all tests
pytest

# Run fast tests only
pytest -m "not slow"

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific category
pytest -m unit              # Unit tests
pytest -m integration       # Integration tests  
pytest -m ai                # AI quality tests

# Run specific file
pytest tests/unit/test_config.py -v
```

## Test File Location Map

| What to Test | File Path |
|--------------|-----------|
| Config validation | `tests/unit/test_config.py` |
| LLM setup | `tests/unit/test_llm.py` |
| CSV processing | `tests/unit/test_ingestion.py` |
| Agent initialization | `tests/unit/test_agents.py` |
| MinIO operations | `tests/integration/test_minio.py` |
| ChromaDB | `tests/integration/test_chromadb.py` |
| RAG pipeline | `tests/integration/test_rag_pipeline.py` |
| Agent outputs | `tests/ai/test_agent_quality.py` |

## Before Running Tests

```bash
# Start Docker services
docker-compose up -d

# Verify services
docker ps                    # Should show minio + chromadb
curl http://localhost:9000   # MinIO
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB

# Verify Ollama (for AI tests)
ollama list                  # Should show llama3.2:3b, bge-m3:567m
```

## Test Status

- ✅ Unit Tests: **34/35 passing (97%)**
- ✅ Integration Tests: **Ready**
- ✅ AI Tests: **Ready** (requires Ollama)
- ✅ Total Tests: **60+**

## Common Issues

| Error | Solution |
|-------|----------|
| ChromaDB connection failed | `docker-compose up -d` |
| Ollama not available | `ollama serve` |
| Tests too slow | `pytest -m "not slow"` |
| Import errors | `uv pip install pytest pytest-cov` |

## Writing New Tests

```python
# tests/unit/test_example.py
import pytest

@pytest.mark.unit
def test_my_feature(sample_csv_data):
    """Test description"""
    # Your test here
    assert True
```

## Documentation

- Full Guide: `TESTING_GUIDE.md`
- Summary: `TEST_SUITE_SUMMARY.md`
- Fixtures: `tests/fixtures/README.md`
