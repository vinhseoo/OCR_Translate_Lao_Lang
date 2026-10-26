# ====================================================================
# Script tu dong khoi chay Ung dung Web OCR Tieng Lao (Streamlit)
# Tu dong nhan dien Python moi truong ao, Python he thong hoac Python pgAdmin 4
# ====================================================================

$ProjectRoot = $PSScriptRoot
Set-Location -Path $ProjectRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " [LAO OCR & EDUCATIONAL TRANSLATION SYSTEM - WEB APP] " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Danh sach cac duong dan Python kha di
$pythonCandidates = @(
    "$ProjectRoot\.venv\Scripts\python.exe",
    "$env:LOCALAPPDATA\Programs\pgAdmin 4\python\python.exe",
    "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe",
    "C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe",
    "C:\Program Files\PostgreSQL\16\pgAdmin 4\python\python.exe"
)

$targetPython = $null

# Kiem tra python trong PATH truoc (loai tru alias rong cua WindowsApps)
$sysPython = Get-Command python -ErrorAction SilentlyContinue
if ($sysPython -and $sysPython.Source -notlike "*WindowsApps*") {
    $targetPython = "python"
} else {
    foreach ($candidate in $pythonCandidates) {
        if (Test-Path -Path $candidate) {
            $targetPython = $candidate
            break
        }
    }
}

if (-not $targetPython) {
    Write-Host "[LOI] Khong tim thay Python kha dung tren he thong!" -ForegroundColor Red
    Write-Host "Vui long cai dat: winget install Python.Python.3.11 roi mo lai PowerShell." -ForegroundColor Yellow
    Exit 1
}

Write-Host "[1/2] Nhan dien moi truong Python:" -ForegroundColor Green
Write-Host "      -> $targetPython" -ForegroundColor Gray

# 2. Khoi chay Streamlit app
Write-Host "[2/2] Dang khoi dong Web Server Streamlit..." -ForegroundColor Green
Write-Host "      -> Trinh duyet se tu dong mo http://localhost:8501" -ForegroundColor Cyan
Write-Host "      -> Nhan Ctrl + C tai cua so nay khi muon dung server." -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan

& $targetPython -m streamlit run "$ProjectRoot\app.py"
