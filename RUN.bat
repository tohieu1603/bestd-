@echo off
cls
echo ========================================
echo    BACKEND SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/api/docs
echo.
echo Nhan Ctrl+C de dung server
echo ========================================
echo.

venv\Scripts\python.exe manage.py runserver

pause
