@echo off
chcp 65001 >nul
title Lao OCR & Educational Translation System - Web App

echo ============================================================
echo  🇱🇦 KHOI CHAY HE THONG LAO OCR ^& EDUCATIONAL TRANSLATION
echo ============================================================

cd /d "%~dp0"

set "TARGET_PYTHON="

if exist ".venv\Scripts\python.exe" (
    set "TARGET_PYTHON=.venv\Scripts\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\pgAdmin 4\python\python.exe" (
    set "TARGET_PYTHON=%LOCALAPPDATA%\Programs\pgAdmin 4\python\python.exe"
) else if exist "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" (
    set "TARGET_PYTHON=C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe"
) else if exist "C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe" (
    set "TARGET_PYTHON=C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe"
) else if exist "C:\Program Files\PostgreSQL\16\pgAdmin 4\python\python.exe" (
    set "TARGET_PYTHON=C:\Program Files\PostgreSQL\16\pgAdmin 4\python\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "TARGET_PYTHON=python"
    )
)

if "%TARGET_PYTHON%"=="" (
    echo [LOI] Khong tim thay Python kha dung tren he thong!
    echo Vui long cai dat Python 3.10 hoac 3.11 bang winget:
    echo   winget install Python.Python.3.11
    pause
    exit /b 1
)

echo [1/2] Nhan dien Python: %TARGET_PYTHON%
echo [2/2] Dang khoi chay Streamlit Web App...
echo Trinh duyet se tu dong mo http://localhost:8501
"%TARGET_PYTHON%" -m streamlit run app.py

pause
