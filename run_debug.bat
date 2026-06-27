@echo off
title Brain Tumor — Debug Mode
call venv\Scripts\activate.bat
set FLASK_ENV=development
set FLASK_DEBUG=1
echo Running in DEBUG mode at http://localhost:5000
python app.py
pause
