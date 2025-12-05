# 🧪 Complete Test Commands Reference

**Quick access to all test commands for the Procurement Assistant project**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Run All Tests](#run-all-tests)
4. [Run by Category](#run-by-category)
5. [Run Specific Files](#run-specific-files)
6. [Run Specific Tests](#run-specific-tests)
7. [Coverage Reports](#coverage-reports)
8. [Advanced Options](#advanced-options)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Before Running Tests:

```bash
# 1. Ensure test dependencies are installed
uv pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests

# Or using pip
pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests
```

### Start Required Services:

```bash
# 2. Start Docker services (for integration & AI tests)
docker-compose up -d

# 3. Verify services are running
docker ps

# 4. Ensure Ollama is running (for AI tests)
ollama serve

# 5. Verify Ollama has required models
ollama list
# Should show: llama3.2:3b and bge-m3:567m
```

---

## Quick Start

### Run Everything (All 63 tests):

```bash
# Navigate to project directory
cd "D:\AI Projects\Procurement_Assistant"

# Run all tests
pytest

# With verbose output
pytest -v

# With quiet output (just summary)
pytest -q
```

**Expected:** 63 passed, 1 warning in ~140 seconds

---

## Run All Tests

### 1. All Tests (Default):
```bash
pytest
```

### 2. All Tests with Verbose Output:
```bash
pytest -v
```

### 3. All Tests with Detailed Output:
```bash
pytest -vv
```

### 4. All Tests with Coverage:
```bash
pytest --cov=backend --cov-report=term-missing
```

### 5. All Tests with HTML Coverage Report:
```bash
pytest --cov=backend --cov-report=html
start htmlcov/index.html
```

---

## Run by Category

### Unit Tests Only (35 tests, ~6s):
```bash
# Fast tests, minimal dependencies
pytest tests/unit/ -v

# Or using marker
pytest -m unit -v
```

**When to use:** During development, before every commit

---

### Integration Tests Only (17 tests, ~41s):
```bash
# Requires Docker services running
pytest tests/integration/ -v

# Or using marker
pytest -m integration -v
```

**Prerequisites:** `docker-compose up -d`

**When to use:** Before deployment, after changing database code

---

### AI Quality Tests Only (11 tests, ~90s):
```bash
# Requires Ollama running
pytest tests/ai/ -v

# Or using marker
pytest -m ai -v
```

**Prerequisites:** Ollama running with models loaded

**When to use:** After modifying agents, before major releases

---

### Skip Slow Tests:
```bash
# Run only fast tests
pytest -m "not slow" -v
```

---

## Run Specific Files

### Configuration Tests:
```bash
pytest tests/unit/test_config.py -v
```

### LLM Initialization Tests:
```bash
pytest tests/unit/test_llm.py -v
```

### Data Ingestion Tests:
```bash
pytest tests/unit/test_ingestion.py -v
```

### Agent Tests:
```bash
pytest tests/unit/test_agents.py -v
```

### MinIO Integration Tests:
```bash
pytest tests/integration/test_minio.py -v
```

### ChromaDB Tests:
```bash
pytest tests/integration/test_chromadb.py -v
```

### RAG Pipeline Tests:
```bash
pytest tests/integration/test_rag_pipeline.py -v
```

### AI Agent Quality Tests:
```bash
pytest tests/ai/test_agent_quality.py -v
```

---

## Run Specific Tests

### Run Single Test Function:
```bash
# Format: pytest path/to/file.py::TestClass::test_function -v

# Example: Test config defaults
pytest tests/unit/test_config.py::TestConfig::test_default_values -v

# Example: Test MinIO upload
pytest tests/integration/test_minio.py::TestMinIOFileOperations::test_upload_file -v

# Example: Test agent quality
pytest tests/ai/test_agent_quality.py::TestAgentOutputQuality::test_spend_agent_output_length -v
```

### Run Tests Matching Pattern:
```bash
# Run all tests with "minio" in the name
pytest -k "minio" -v

# Run all tests with "agent" in the name
pytest -k "agent" -v

# Run all tests with "upload" in the name
pytest -k "upload" -v

# Run tests matching multiple patterns
pytest -k "upload or download" -v
```

### Run Tests in a Class:
```bash
# Format: pytest path/to/file.py::TestClassName -v

# Example: All config tests
pytest tests/unit/test_config.py::TestConfig -v

# Example: All MinIO file operation tests
pytest tests/integration/test_minio.py::TestMinIOFileOperations -v
```

---

## Coverage Reports

### 1. Terminal Coverage Summary:
```bash
pytest --cov=backend
```

### 2. Detailed Missing Lines:
```bash
pytest --cov=backend --cov-report=term-missing
```

### 3. HTML Coverage Report:
```bash
# Generate report
pytest --cov=backend --cov-report=html

# Open in browser (Windows)
start htmlcov/index.html

# Or manually open: htmlcov/index.html
```

### 4. Coverage with Minimum Threshold:
```bash
# Fail if coverage below 60%
pytest --cov=backend --cov-fail-under=60
```

### 5. Coverage for Specific Module:
```bash
# Only backend/agents.py
pytest --cov=backend.agents --cov-report=term-missing
```

---

## Advanced Options

### Parallel Execution (Faster):
```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -n 4

# Auto-detect number of CPUs
pytest -n auto
```

### Stop on First Failure:
```bash
# Exit immediately on first failure
pytest -x

# Exit after 3 failures
pytest --maxfail=3
```

### Show Local Variables on Failure:
```bash
pytest -l
```

### Disable Warnings:
```bash
pytest --disable-warnings
```

### Show Print Statements:
```bash
# Show print() and logger output
pytest -s

# Or
pytest --capture=no
```

### Dry Run (Collect Tests Without Running):
```bash
# See what tests would run
pytest --collect-only

# Quiet mode
pytest --co -q
```

### Rerun Failed Tests:
```bash
# Install pytest-rerunfailures
pip install pytest-rerunfailures

# Rerun failed tests up to 3 times
pytest --reruns 3
```

### Custom Timeout:
```bash
# Timeout individual tests after 10 seconds
pytest --timeout=10
```

---

## Combination Commands

### Development Workflow:
```bash
# Run fast tests during development
pytest tests/unit/ -v --tb=short

# Run all tests before commit
pytest -v

# Full validation before deploy
pytest --cov=backend --cov-report=html
```

### CI/CD Pipeline:
```bash
# What CI/CD should run
pytest -v --cov=backend --cov-report=xml --cov-fail-under=60
```

### Debugging Failures:
```bash
# Detailed failure information
pytest -vv --tb=long -l

# Stop on first failure with full output
pytest -x -vv --tb=long -s
```

---

## Output Control

### Minimal Output:
```bash
pytest -q
```

### Standard Output:
```bash
pytest
```

### Verbose Output:
```bash
pytest -v
```

### Very Verbose Output:
```bash
pytest -vv
```

### Custom Format:
```bash
# Short traceback
pytest --tb=short

# Line-only traceback
pytest --tb=line

# No traceback
pytest --tb=no

# Full traceback
pytest --tb=long
```

---

## Troubleshooting

### Common Issues & Solutions:

#### ChromaDB Connection Failed:
```bash
# Check if Docker is running
docker ps

# Restart Docker services
docker-compose down
docker-compose up -d

# Verify ChromaDB is accessible
Invoke-WebRequest -Uri http://localhost:8000/api/v1/version
```

#### Ollama Not Available:
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Verify models are pulled
ollama pull llama3.2:3b
ollama pull bge-m3:567m
```

#### Import Errors:
```bash
# Reinstall dependencies
uv pip install -r pyproject.toml

# Or
pip install -e .
```

#### Permission Errors (MinIO):
```bash
# Clear test files
# Access MinIO console at http://localhost:9001
# Login: minioadmin / minioadmin
# Delete files starting with "test_"
```

#### Tests Running Slow:
```bash
# Skip slow AI tests
pytest -m "not slow" -v

# Run only unit tests
pytest tests/unit/ -v

# Use parallel execution
pytest -n auto
```

#### Unicode/Encoding Errors (Windows):
```bash
# Use quiet mode to avoid display issues
pytest -q

# Or set environment variable
set PYTHONIOENCODING=utf-8
pytest -v
```

---

## Test Markers Reference

Available markers for filtering tests:

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests (needs Docker)
- `@pytest.mark.ai` - AI quality tests (needs Ollama)
- `@pytest.mark.slow` - Tests taking > 5 seconds

### Using Markers:
```bash
# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run AI tests only
pytest -m ai

# Exclude slow tests
pytest -m "not slow"

# Combine markers
pytest -m "unit or integration"
```

---

## Daily Workflow Examples

### Morning Code Check:
```bash
# Quick validation (6 seconds)
pytest tests/unit/ -q
```

### Before Committing:
```bash
# Full validation (2-3 minutes)
pytest -v
```

### Before Deploying:
```bash
# Complete validation with coverage
pytest --cov=backend --cov-report=html --cov-fail-under=60
start htmlcov/index.html
```

### After Modifying Agents:
```bash
# Test agents specifically
pytest tests/unit/test_agents.py tests/ai/ -v
```

### After Changing Database Code:
```bash
# Test integrations
pytest tests/integration/ -v
```

---

## Continuous Testing (Watch Mode)

### Install pytest-watch:
```bash
pip install pytest-watch
```

### Auto-run tests on file changes:
```bash
# Watch and run all tests
ptw

# Watch and run unit tests only
ptw -- tests/unit/

# Watch with specific options
ptw -- -v --tb=short
```

---

## Quick Reference Card

```bash
# ============================================
# MOST COMMON COMMANDS
# ============================================

# Run everything
pytest

# Run unit tests (fast)
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run AI tests
pytest tests/ai/ -v

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific file
pytest tests/unit/test_config.py -v

# Run specific test
pytest tests/unit/test_config.py::TestConfig::test_default_values -v

# Skip slow tests
pytest -m "not slow" -v

# Stop on first failure
pytest -x

# Quiet mode
pytest -q
```

---

## Test Execution Time

Expected durations (approximate):

| Category | Tests | Duration | Command |
|----------|-------|----------|---------|
| Unit Tests | 35 | ~6s | `pytest tests/unit/` |
| Integration Tests | 17 | ~41s | `pytest tests/integration/` |
| AI Quality Tests | 11 | ~90s | `pytest tests/ai/` |
| **All Tests** | **63** | **~140s** | `pytest` |

---

## Creating Test Reports

### JUnit XML Report (for CI):
```bash
pytest --junitxml=test-results.xml
```

### JSON Report:
```bash
# Install plugin
pip install pytest-json-report

# Generate report
pytest --json-report --json-report-file=test-report.json
```

### HTML Report:
```bash
# Install plugin
pip install pytest-html

# Generate report
pytest --html=report.html --self-contained-html
```

---

## Environment Variables

Useful environment variables for testing:

```bash
# Set Python encoding (Windows)
set PYTHONIOENCODING=utf-8

# Disable pytest cache
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

# Set test database
set CHROMA_HOST=localhost
set CHROMA_PORT=8000

# Set MinIO credentials
set MINIO_ENDPOINT=localhost:9000
set MINIO_ACCESS_KEY=minioadmin
set MINIO_SECRET_KEY=minioadmin
```

---

## Summary

**Total Tests:** 63
- Unit: 35
- Integration: 17  
- AI Quality: 11

**All commands are in this file for quick reference!**

**Most Important Commands:**
1. `pytest` - Run everything
2. `pytest tests/unit/ -v` - Quick validation
3. `pytest --cov=backend --cov-report=html` - Coverage report

**Save this file for future reference!** 📌
