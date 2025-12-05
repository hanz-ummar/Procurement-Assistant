@echo off
REM ========================================
REM Procurement Assistant - Test Runner
REM Quick access to common test commands
REM ========================================

echo.
echo ========================================
echo    Procurement Assistant Test Suite
echo ========================================
echo.
echo Select test category to run:
echo.
echo  1. Run ALL tests (63 tests, ~2.5 mins)
echo  2. Run UNIT tests only (35 tests, ~6 secs)
echo  3. Run INTEGRATION tests (17 tests, ~41 secs)
echo  4. Run AI QUALITY tests (11 tests, ~90 secs)
echo  5. Run SPECIFIC file (choose from list)
echo  6. Generate COVERAGE report
echo  7. Quick validation (unit tests only)
echo  8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto all
if "%choice%"=="2" goto unit
if "%choice%"=="3" goto integration
if "%choice%"=="4" goto ai
if "%choice%"=="5" goto specific
if "%choice%"=="6" goto coverage
if "%choice%"=="7" goto quick
if "%choice%"=="8" goto end
goto invalid

:all
echo.
echo Running ALL 63 tests...
pytest -v
goto end

:unit
echo.
echo Running UNIT tests (35 tests)...
pytest tests/unit/ -v
goto end

:integration
echo.
echo Checking Docker services...
docker ps --filter "name=procurement"
echo.
echo Starting Integration tests...
pytest tests/integration/ -v
goto end

:ai
echo.
echo Checking Ollama...
ollama list
echo.
echo Starting AI Quality tests...
pytest tests/ai/ -v
goto end

:specific
echo.
echo Available test files:
echo  1. tests/unit/test_config.py
echo  2. tests/unit/test_llm.py
echo  3. tests/unit/test_ingestion.py
echo  4. tests/unit/test_agents.py
echo  5. tests/integration/test_minio.py
echo  6. tests/integration/test_chromadb.py
echo  7. tests/integration/test_rag_pipeline.py
echo  8. tests/ai/test_agent_quality.py
echo.
set /p file="Enter file number (1-8): "

if "%file%"=="1" pytest tests/unit/test_config.py -v
if "%file%"=="2" pytest tests/unit/test_llm.py -v
if "%file%"=="3" pytest tests/unit/test_ingestion.py -v
if "%file%"=="4" pytest tests/unit/test_agents.py -v
if "%file%"=="5" pytest tests/integration/test_minio.py -v
if "%file%"=="6" pytest tests/integration/test_chromadb.py -v
if "%file%"=="7" pytest tests/integration/test_rag_pipeline.py -v
if "%file%"=="8" pytest tests/ai/test_agent_quality.py -v
goto end

:coverage
echo.
echo Generating coverage report...
pytest --cov=backend --cov-report=html
echo.
echo Opening coverage report in browser...
start htmlcov/index.html
goto end

:quick
echo.
echo Running quick validation (unit tests only)...
pytest tests/unit/ -q
goto end

:invalid
echo.
echo Invalid choice! Please select 1-8.
pause
goto end

:end
echo.
echo ========================================
echo Test run complete!
echo ========================================
echo.
pause
