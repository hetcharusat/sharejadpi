# Build ShareJadPi Installer
# This creates a professional Windows installer (.exe)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ShareJadPi v3.0.0 - Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Inno Setup is installed
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if (-not (Test-Path $innoSetupPath)) {
    Write-Host "ERROR: Inno Setup not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Inno Setup from:" -ForegroundColor Yellow
    Write-Host "https://jrsoftware.org/isdl.php" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "[OK] Inno Setup found" -ForegroundColor Green
Write-Host ""

# Check if .exe exists
$exePath = "dist\ShareJadPi-3.0.0.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "ERROR: ShareJadPi-3.0.0.exe not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please build the .exe first by running:" -ForegroundColor Yellow
    Write-Host "  .\build_v3.ps1" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}

Write-Host "[OK] ShareJadPi-3.0.0.exe found" -ForegroundColor Green
Write-Host ""

# Create output directory
if (-not (Test-Path "installer_output")) {
    New-Item -ItemType Directory -Path "installer_output" | Out-Null
}

Write-Host "Building installer..." -ForegroundColor Yellow
Write-Host ""

# Build the installer
$scriptPath = Join-Path $PSScriptRoot "ShareJadPi-Installer.iss"
& $innoSetupPath $scriptPath

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Installer created!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    $installerPath = "installer_output\ShareJadPi-3.0.0-Setup.exe"
    if (Test-Path $installerPath) {
        $size = (Get-Item $installerPath).Length / 1MB
        Write-Host "Installer: $installerPath" -ForegroundColor Cyan
        Write-Host "Size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "This installer includes:" -ForegroundColor Yellow
        Write-Host "  [+] ShareJadPi-3.0.0.exe" -ForegroundColor White
        Write-Host "  [+] Automatic firewall configuration" -ForegroundColor White
        Write-Host "  [+] Context menu integration (optional)" -ForegroundColor White
        Write-Host "  [+] Autostart with Windows (optional)" -ForegroundColor White
        Write-Host "  [+] Desktop shortcut (optional)" -ForegroundColor White
        Write-Host "  [+] All documentation files" -ForegroundColor White
        Write-Host "  [+] Uninstaller" -ForegroundColor White
        Write-Host ""
        Write-Host "Users can now install ShareJadPi with one click!" -ForegroundColor Green
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "ERROR: Installer build failed!" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

pause
