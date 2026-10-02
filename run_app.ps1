# ====================================================================
# Script tự động khởi chạy Ứng dụng Web OCR Tiếng Lào (Streamlit)
# ====================================================================

$ProjectRoot = $PSScriptRoot
Set-Location -Path $ProjectRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 🇱🇦 KHỞI CHẠY HỆ THỐNG LAO OCR & EDUCATIONAL TRANSLATION " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Kiểm tra môi trường ảo .venv
if (Test-Path -Path "$ProjectRoot\.venv\Scripts\Activate.ps1") {
    Write-Host "[1/3] Dang kich hoat moi truong ao .venv..." -ForegroundColor Green
    & "$ProjectRoot\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "[CANH BAO] Chua tim thay thu muc .venv!" -ForegroundColor Yellow
    Write-Host "Kiem tra xem he thong da co python chua..." -ForegroundColor Gray
    
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Host "[LOI] May chua cai dat Python hoac chua them vao PATH." -ForegroundColor Red
        Write-Host "Vui long chay: winget install Python.Python.3.11 roi mo lai PowerShell." -ForegroundColor Red
        Exit 1
    }

    Write-Host "Dang tao moi truong ao .venv lan dau..." -ForegroundColor Cyan
    python -m venv .venv
    & "$ProjectRoot\.venv\Scripts\Activate.ps1"
    
    Write-Host "Dang cai dat dependencies tu requirements.txt..." -ForegroundColor Cyan
    pip install --upgrade pip
    pip install -r requirements.txt
}

# 2. Kiểm tra Streamlit
Write-Host "[2/3] Kiem tra Streamlit..." -ForegroundColor Green
$streamlitInstalled = python -c "import streamlit; print('OK')" 2>$null
if ($streamlitInstalled -ne "OK") {
    Write-Host "Streamlit chua duoc cai dat. Dang tien hanh cai dat requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 3. Chạy Streamlit app
Write-Host "[3/3] Dang khoi dong Web Server Streamlit..." -ForegroundColor Green
Write-Host "Trinh duyet se tu dong mo http://localhost:8501 (Nhan Ctrl+C de dung)" -ForegroundColor Cyan
python -m streamlit run app.py
