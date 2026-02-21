@echo off
echo ========================================
echo AGENTIC SALES AI - SETUP SCRIPT
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Login==0.6.3
pip install Werkzeug==3.0.1
pip install google-generativeai
pip install requests
pip install python-dotenv
echo [OK] All dependencies installed
echo.

REM Create directories
echo Creating directories...
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist static\generated_assets mkdir static\generated_assets
if not exist templates mkdir templates
if not exist ai_services mkdir ai_services
if not exist api mkdir api
if not exist database mkdir database
if not exist n8n_workflows mkdir n8n_workflows
echo [OK] Directories created
echo.

REM Create .gitkeep
type nul > static\generated_assets\.gitkeep

REM Check .env file
echo Checking .env file...
if exist .env (
    echo [OK] .env file exists
    findstr /C:"GOOGLE_GEMINI_API_KEY=" .env >nul
    if errorlevel 1 (
        echo [WARNING] Google Gemini API key not configured
        echo Please add your API key to .env file
        echo Get FREE key: https://makersuite.google.com/app/apikey
    ) else (
        echo [OK] Configuration found
    )
) else (
    echo [WARNING] .env file not found
    echo Please create .env file with your configuration
)
echo.

REM Final message
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Update .env file with your Google Gemini API key
echo    Get FREE key: https://makersuite.google.com/app/apikey
echo.
echo 2. Generate a SECRET_KEY:
echo    python -c "import secrets; print(secrets.token_hex(32))"
echo.
echo 3. Start the application:
echo    run.bat
echo.
echo 4. Open in browser:
echo    http://localhost:5000
echo.
echo ========================================
pause