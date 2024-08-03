@echo off
echo Installing Python requirements...

REM Check if pip is installed
where pip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install Python with pip and try again.
    exit /b 1
)

REM Install the required packages
pip install requests colorama sockets concurrent.futures

REM Check if installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo An error occurred during the installation.
    exit /b 1
)

echo All requirements installed successfully.
pause
