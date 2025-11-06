@echo off
chcp 65001 >nul
cls
echo ========================================
echo    TAO ADMIN USER
echo ========================================
echo.
echo Nhap thong tin admin:
echo - Username: admin
echo - Password: admin123
echo.

venv\Scripts\python.exe manage.py createsuperuser

echo.
echo Da tao xong! Bay gio chay: run-backend.bat
pause
