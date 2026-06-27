@echo off
REM ═══════════════════════════════════════════════════════════
REM  Brain Tumor Diagnosis — Start App
REM  Double-click to run the Flask server
REM ═══════════════════════════════════════════════════════════
title Brain Tumor Diagnosis — Running

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   Brain Tumor Diagnosis — Starting...    ║
echo  ╚══════════════════════════════════════════╝
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo  [✓] Virtual environment activated
) else (
    echo  [!] No venv found. Run install.bat first!
    pause
    exit /b 1
)

REM Check model exists
if not exist models\model.h5 (
    echo.
    echo  [!] ERROR: models\model.h5 not found!
    echo      Please place your trained model file at:
    echo      %cd%\models\model.h5
    echo.
    pause
    exit /b 1
)

echo  [✓] model.h5 found
echo.
echo  [*] Starting Flask server...
echo      URL: http://localhost:5000
echo      Press CTRL+C to stop
echo.

python app.py
pause
