@echo off
setlocal
title Exam Scheduler Setup

echo ===================================================
echo      EXAM SCHEDULER - AUTOMATIC SETUP
echo ===================================================
echo.

:: 1. CHECK PREREQUISITES
echo [1/6] Checking required software...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/ and check "Add to PATH".
    pause
    exit /b
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b
)

psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PostgreSQL is not found in PATH.
    echo Please make sure C:\Program Files\PostgreSQL\XX\bin is in your Environment Variables.
    echo Alternatively, just ensure PostgreSQL is installed and we will try to find it.
)

echo Software checks passed.
echo.

:: 2. DATABASE SETUP
echo [2/6] Setting up Database...
set /p PG_PASSWORD="Enter your PostgreSQL Password (created during installation): "

:: Try to find psql if not in path (common issue)
if exist "C:\Program Files\PostgreSQL\17\bin\psql.exe" (
    set PATH=%PATH%;C:\Program Files\PostgreSQL\17\bin
)
if exist "C:\Program Files\PostgreSQL\16\bin\psql.exe" (
    set PATH=%PATH%;C:\Program Files\PostgreSQL\16\bin
)
if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
    set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin
)

set PGPASSWORD=%PG_PASSWORD%

echo Creating database 'exam_scheduler'...
createdb -U postgres exam_scheduler 2>nul
if %errorlevel% neq 0 (
    echo Database might already exist, skipping creation...
)

echo Importing data from backup...
psql -U postgres -d exam_scheduler -f "database/full_backup.sql" >nul 2>&1

if %errorlevel% neq 0 (
    echo [WARNING] There were some errors importing the data.
    echo This might be okay if the data already exists.
) else (
    echo Database imported successfully!
)
echo.

:: 3. BACKEND SETUP
echo [3/6] Setting up Backend...
cd backend

:: Create .env
echo Creating .env file...
copy .env.example .env >nul
:: We should ideally replace password here, but for simplicity we assume localhost access works or user edits it later if complex auth needed. 
:: A simple append to update the url:
echo. >> .env
echo DATABASE_URL=postgresql://postgres:%PG_PASSWORD%@localhost:5432/exam_scheduler>> .env

echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt >nul
cd ..
echo.

:: 4. FRONTEND SETUP
echo [4/6] Setting up Frontend...
cd frontend
echo Installing Node modules (this takes a minute)...
call npm install >nul
cd ..
echo.

:: 5. START SCRIPT
echo ===================================================
echo [5/6] Creating 'start_project.bat' for easy launching...
(
echo @echo off
echo start "Backend API" cmd /k "cd backend ^& venv\Scripts\activate ^& python -m uvicorn app.main:app --reload --port 8000"
echo start "Frontend App" cmd /k "cd frontend ^& npm run dev"
echo echo Project started! Go to http://localhost:3000
echo pause
) > start_project.bat
echo.

echo ===================================================
echo [6/6] SETUP COMPLETE!
echo ===================================================
echo.
echo To run the project:
echo 1. Double-click 'start_project.bat'
echo 2. Open http://localhost:3000
echo.
pause
