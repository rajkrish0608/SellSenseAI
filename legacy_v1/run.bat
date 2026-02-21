@echo off
echo ========================================
echo STARTING AGENTIC SALES AI
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check .env file
if not exist .env (
    echo [WARNING] .env file not found
    echo Please create .env file with configuration
)

echo.
echo Starting Flask application...
echo Press Ctrl+C to stop
echo.

REM Run the application
python app.py