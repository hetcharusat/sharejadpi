# Build ShareJadPi v3.0.0 executable
# Run this script to create a standalone .exe file

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building ShareJadPi v3.0.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
pip show pyinstaller >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host ""
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build the executable
Write-Host ""
Write-Host "Building executable (this may take a few minutes)..." -ForegroundColor Yellow
pyinstaller --clean ShareJadPi-3.0.0.spec

# Check if build was successful
if (Test-Path "dist\ShareJadPi-3.0.0.exe") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location:" -ForegroundColor Cyan
    $exePath = Resolve-Path "dist\ShareJadPi-3.0.0.exe"
    Write-Host "  $exePath" -ForegroundColor White
    Write-Host ""
    $size = (Get-Item "dist\ShareJadPi-3.0.0.exe").Length / 1MB
    $sizeRounded = [math]::Round($size, 2)
    Write-Host "File size: $sizeRounded MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run the executable:" -ForegroundColor Yellow
    Write-Host "  .\dist\ShareJadPi-3.0.0.exe" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Build failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the output above for errors." -ForegroundColor Yellow
    Write-Host ""
}
