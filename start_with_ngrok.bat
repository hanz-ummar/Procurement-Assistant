@echo off
echo ========================================
echo  Procurement Assistant + Ngrok Launcher
echo ========================================
echo.

REM Check if Docker is running
echo [1/4] Checking Docker...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)
echo ✓ Docker is running

REM Start Docker services
echo.
echo [2/4] Starting MinIO and ChromaDB...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Docker services
    pause
    exit /b 1
)
echo ✓ Services started

REM Start Streamlit in background
echo.
echo [3/4] Starting Streamlit app...
start "Procurement Assistant" cmd /k "streamlit run app.py"
echo ✓ Streamlit starting...
echo.
echo Waiting for Streamlit to start (10 seconds)...
timeout /t 10 /nobreak >nul

REM Start ngrok
echo.
echo [4/4] Starting ngrok tunnel...
echo.
echo ========================================
echo  SHARE THIS URL WITH YOUR COLLEAGUE:
echo ========================================
echo.
ngrok http 8501

REM This line only runs after ngrok is stopped (Ctrl+C)
echo.
echo Ngrok stopped. Streamlit is still running.
echo Close the Streamlit window manually if needed.
pause
