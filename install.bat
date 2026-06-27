@echo off
REM ═══════════════════════════════════════════════════════════
REM  Brain Tumor Diagnosis — Windows Installer
REM  Double-click this file to set up the project
REM ═══════════════════════════════════════════════════════════
title Brain Tumor Diagnosis — Setup

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  Brain Tumor Diagnosis — Installing...   ║
echo  ╚══════════════════════════════════════════╝
echo.

REM Create virtual environment
echo  [1/4] Creating virtual environment...
python -m venv venv
echo  [✓] venv created

echo.
echo  [2/4] Activating venv...
call venv\Scripts\activate.bat

echo.
echo  [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo.
echo  [4/4] Installing packages (this may take 3-5 mins)...
pip install -r requirements.txt

echo.
echo  ══════════════════════════════════════════════
echo   Installation complete!
echo.
echo   IMPORTANT: Place your model.h5 in:
echo     models\model.h5
echo.
echo   Then run the app:
echo     run.bat
echo  ══════════════════════════════════════════════
echo.
pause
