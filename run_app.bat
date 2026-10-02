@echo off
chcp 65001 >nul
title Lao OCR & Educational Translation System - Web App

echo ============================================================
echo  🇱🇦 KHOI CHAY HE THONG LAO OCR ^& EDUCATIONAL TRANSLATION
echo ============================================================

cd /d "%~dp0"

IF EXIST ".venv\Scripts\activate.bat" (
    echo [1/2] Dang kich hoat moi truong ao .venv...
    call .venv\Scripts\activate.bat
) ELSE (
    echo [!] Chua tim thay moi truong ao .venv.
    echo Dang khoi tao .venv va cai dat thu vien...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

echo [2/2] Dang khoi chay Streamlit Web App...
python -m streamlit run app.py

pause
