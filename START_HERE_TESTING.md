# 🎯 Test Commands - Ultra Quick Reference

## ⚡ Top 5 Commands You'll Use Every Day

```bash
# 1. Quick validation (6 seconds)
pytest tests/unit/ -q

# 2. Run everything (2-3 minutes)
pytest -v

# 3. Run specific category
pytest tests/integration/ -v

# 4. Generate coverage report
pytest --cov=backend --cov-report=html

# 5. Interactive mode (Windows)
.\run_tests.bat
```

---

## 📚 Where to Find What You Need

| **I Want To...** | **Use This** |
|------------------|--------------|
| 🎮 **Run tests the easy way** | `run_tests.bat` (double-click) |
| 📋 **See common commands** | `TEST_CHEAT_SHEET.md` (1 page) |
| 📖 **Learn everything** | `TEST_COMMANDS.md` (complete guide) |
| 🎓 **Understand the system** | `TESTING_GUIDE.md` |
| 📊 **See test results** | `INTEGRATION_TEST_RESULTS.md` |
| 🗺️ **Find documentation** | `TEST_DOCUMENTATION_INDEX.md` |

---

## 🚀 Copy-Paste Ready Commands

### Prerequisites (One-Time Setup)
```bash
# Install test dependencies
uv pip install pytest pytest-cov pytest-asyncio pytest-timeout pytest-mock requests

# Start Docker services
docker-compose up -d

# Verify Ollama
ollama list
```

### Daily Workflow
```bash
# Morning: Quick check
pytest tests/unit/ -q

# Before commit: Full validation
pytest -v

# Before deploy: With coverage
pytest --cov=backend --cov-report=html && start htmlcov/index.html
```

### Test Categories
```bash
# Unit tests (35 tests, ~6s)
pytest tests/unit/ -v

# Integration tests (17 tests, ~41s)
pytest tests/integration/ -v

# AI quality tests (11 tests, ~90s)
pytest tests/ai/ -v

# Skip slow tests
pytest -m "not slow" -v
```

### Specific Files
```bash
# Config
pytest tests/unit/test_config.py -v

# Agents
pytest tests/unit/test_agents.py -v

# MinIO
pytest tests/integration/test_minio.py -v

# AI Quality
pytest tests/ai/test_agent_quality.py -v
```

---

## 📊 Expected Results

| Command | Tests | Duration | Expected |
|---------|-------|----------|----------|
| `pytest` | 63 | ~140s | All pass ✅ |
| `pytest tests/unit/` | 35 | ~6s | All pass ✅ |
| `pytest tests/integration/` | 17 | ~41s | All pass ✅ |
| `pytest tests/ai/` | 11 | ~90s | All pass ✅ |

---

## 🎯 Your Testing Toolkit

**Created for you:**
1. ✅ `TEST_COMMANDS.md` - 500+ lines of every command
2. ✅ `TEST_CHEAT_SHEET.md` - One-page quick reference  
3. ✅ `run_tests.bat` - Interactive Windows runner
4. ✅ `TESTING_GUIDE.md` - Complete guide
5. ✅ `TEST_DOCUMENTATION_INDEX.md` - Navigation guide

**All in:** `D:\AI Projects\Procurement_Assistant\`

---

## 💡 Remember

- 🎯 **Most Common:** `pytest tests/unit/ -q` (quick check)
- 🚀 **Before Commit:** `pytest -v` (full validation)
- 📊 **Before Deploy:** `pytest --cov=backend --cov-report=html`
- 🎮 **Easiest Way:** `run_tests.bat` (Windows interactive menu)

**Save this file as your go-to reference!** 📌
