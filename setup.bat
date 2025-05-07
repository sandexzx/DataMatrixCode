@echo off
setlocal enabledelayedexpansion

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
echo Found Python version: !PYTHON_VERSION!

echo Checking virtualenv...
python -m pip show virtualenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing virtualenv...
    python -m pip install virtualenv --user
    if %errorlevel% neq 0 (
        echo Error: Failed to install virtualenv
        pause
        exit /b 1
    )
    
    :: Add user's Python Scripts directory to PATH
    for /f "tokens=*" %%i in ('python -c "import site; print(site.getusersitepackages().replace('Lib\\site-packages', 'Scripts'))"') do set USER_SCRIPTS=%%i
    set "PATH=!USER_SCRIPTS!;!PATH!"
)

echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)
python -m virtualenv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Error: Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo You can now run the script using run.bat
echo.
pause 