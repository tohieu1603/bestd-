@echo off
chcp 65001 >nul
echo ========================================
echo    BACKEND SERVER ĐANG CHẠY
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/api/docs
echo Admin Panel: http://localhost:8000/admin
echo.
echo Nhấn Ctrl+C để dừng server
echo ========================================
echo.

venv\Scripts\python.exe manage.py runserver

pause
