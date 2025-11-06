@echo off
cls
echo ========================================
echo    SETUP BACKEND - BUOC 1
echo ========================================
echo.

cd /d "%~dp0"

echo Dang o thu muc: %CD%
echo.

echo [1] Tao virtual environment...
if not exist venv (
    python -m venv venv
    echo - Da tao venv!
) else (
    echo - Venv da ton tai!
)

echo.
echo [2] Cai dat Django...
venv\Scripts\python.exe -m pip install --quiet Django django-ninja django-cors-headers python-dotenv pydantic PyJWT bcrypt pillow

echo.
echo [3] Tao database...
if not exist db.sqlite3 (
    venv\Scripts\python.exe manage.py makemigrations
    venv\Scripts\python.exe manage.py migrate
    echo - Database da duoc tao!
) else (
    echo - Database da ton tai!
)

echo.
echo ========================================
echo    SETUP THANH CONG!
echo ========================================
echo.
echo Bay gio chay: CREATE-USER.bat
echo.
pause
