@echo off
echo Starting Procurement Assistant...

:: Activate virtual environment
:: uv handles virtual environment automatically

:: Start Docker containers
docker-compose up -d

:: Run Streamlit application
echo Starting Streamlit...
uv run streamlit run app.py

pause
