@echo off
cls
echo ========================================
echo    TAO ADMIN USER
echo ========================================
echo.

cd /d "%~dp0"

echo Nhap thong tin:
echo - Username: admin
echo - Email: (Enter de bo qua)
echo - Password: admin123
echo.

venv\Scripts\python.exe manage.py createsuperuser

echo.
echo ========================================
if errorlevel 1 (
    echo CO LOI XAY RA!
    echo Hay chay lai SETUP-BACKEND.bat truoc
) else (
    echo DA TAO USER THANH CONG!
    echo Bay gio chay: RUN.bat
)
echo ========================================
echo.
pause
