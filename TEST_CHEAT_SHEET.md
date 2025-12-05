# 📋 Test Commands Cheat Sheet

## 🚀 Quick Start
```bash
pytest                    # Run all 63 tests
pytest -v                 # Verbose output
pytest -q                 # Quiet mode (summary only)
```

## 📂 By Category
```bash
pytest tests/unit/        # Unit tests (35, ~6s)
pytest tests/integration/ # Integration tests (17, ~41s)
pytest tests/ai/          # AI quality tests (11, ~90s)
```

## 📄 Specific Files
```bash
pytest tests/unit/test_config.py -v         # Config tests
pytest tests/unit/test_agents.py -v         # Agent tests
pytest tests/integration/test_minio.py -v   # MinIO tests
pytest tests/ai/test_agent_quality.py -v    # AI quality
```

## 🎯 Using Markers
```bash
pytest -m unit            # Unit tests only
pytest -m integration     # Integration only
pytest -m ai              # AI tests only
pytest -m "not slow"      # Skip slow tests
```

## 📊 Coverage
```bash
pytest --cov=backend                           # Show coverage
pytest --cov=backend --cov-report=html         # HTML report
pytest --cov=backend --cov-report=term-missing # Show missing lines
```

## 🔍 Advanced
```bash
pytest -k "minio"         # Tests matching "minio"
pytest -x                 # Stop on first failure
pytest -v --tb=short      # Verbose with short traceback
pytest -s                 # Show print statements
```

## 🛠️ Prerequisites
```bash
# Install dependencies
uv pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests

# Start services
docker-compose up -d      # Start MinIO + ChromaDB
ollama serve              # Start Ollama (for AI tests)
```

## 📈 Expected Results
- **All tests:** 63 passed (~140s)
- **Unit tests:** 35 passed (~6s)
- **Integration:** 17 passed (~41s)
- **AI tests:** 11 passed (~90s)

## 💡  Most Used Commands
```bash
# Daily development
pytest tests/unit/ -v

# Before commit
pytest

# Before deploy
pytest --cov=backend --cov-report=html

# Quick check
pytest -q
```

## 🎮 Interactive Mode (Windows)
```bash
run_tests.bat             # Interactive menu
```

## 📚 Full Documentation
See `TEST_COMMANDS.md` for complete reference with all options!
