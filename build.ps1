# Build ShareJadPi Executable
# Run this from the project root

Write-Host "Building ShareJadPi v3.1.1..." -ForegroundColor Cyan

# Check if PyInstaller is installed
pip show pyinstaller >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Change to build_tools directory
Push-Location build_tools

# Build
Write-Host "Running PyInstaller..." -ForegroundColor Yellow
pyinstaller --clean ShareJadPi-3.1.1.spec

# Return to root
Pop-Location

# Check result
if (Test-Path "dist\ShareJadPi-3.1.1.exe") {
    Write-Host ""
    Write-Host "✓ Build successful!" -ForegroundColor Green
    Write-Host "Output: dist\ShareJadPi-3.1.1.exe" -ForegroundColor Cyan
    $size = (Get-Item "dist\ShareJadPi-3.1.1.exe").Length / 1MB
    Write-Host "Size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✗ Build failed!" -ForegroundColor Red
}
