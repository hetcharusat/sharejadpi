# Build ShareJadPi Executable
# Run this from the project root

Write-Host "Building ShareJadPi v4.5.0..." -ForegroundColor Cyan

# Use project venv Python if available
$projectRoot = $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $python = $venvPython
} else {
    $python = "python"
}

# Prepare output/work directories
$distPath = Join-Path $projectRoot "dist"
$workPath = Join-Path $projectRoot "build\pyinstaller\ShareJadPi-4.5.0"
if (-not (Test-Path $distPath)) { New-Item -ItemType Directory -Path $distPath | Out-Null }
if (-not (Test-Path $workPath)) { New-Item -ItemType Directory -Path $workPath | Out-Null }

# Check if PyInstaller is installed
$null = & $python -m pip show pyinstaller 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    & $python -m pip install pyinstaller
}

# Change to build_tools directory
Push-Location build_tools

# Build
Write-Host "Running PyInstaller..." -ForegroundColor Yellow
& $python -m PyInstaller --clean --distpath "$distPath" --workpath "$workPath" ShareJadPi-4.5.0.spec

# Return to root
Pop-Location

# Check result
if (Test-Path "dist\ShareJadPi-4.5.0.exe") {
    Write-Host ""
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Output: dist\ShareJadPi-4.5.0.exe" -ForegroundColor Cyan
    $size = (Get-Item "dist\ShareJadPi-4.5.0.exe").Length / 1MB
    Write-Host "Size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "NOTE: cloudflared.exe is bundled and extracted to sys._MEIPASS." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
}
