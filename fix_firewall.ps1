# ShareJadPi Firewall Fix
# Run this as Administrator to allow network access

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ShareJadPi - Firewall Fix" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "How to run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click on 'fix_firewall.ps1'" -ForegroundColor Yellow
    Write-Host "2. Select 'Run with PowerShell (Admin)'" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "Running as Administrator... Good!" -ForegroundColor Green
Write-Host ""

# Get the exe path
$exePath = Join-Path $PSScriptRoot "dist\ShareJadPi-3.0.0.exe"

if (-not (Test-Path $exePath)) {
    Write-Host "ERROR: Cannot find ShareJadPi-3.0.0.exe at:" -ForegroundColor Red
    Write-Host $exePath -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host "Found exe at: $exePath" -ForegroundColor Green
Write-Host ""

# Remove any existing rules (in case of duplicates)
Write-Host "Removing any old firewall rules..." -ForegroundColor Yellow
try {
    Remove-NetFirewallRule -DisplayName "ShareJadPi - Inbound" -ErrorAction SilentlyContinue
    Remove-NetFirewallRule -DisplayName "ShareJadPi - Outbound" -ErrorAction SilentlyContinue
    Write-Host "Old rules removed (if any existed)" -ForegroundColor Green
} catch {
    Write-Host "No old rules to remove" -ForegroundColor Gray
}
Write-Host ""

# Add new firewall rules
Write-Host "Adding firewall rules for ShareJadPi..." -ForegroundColor Yellow
Write-Host ""

try {
    # Inbound rule (allows incoming connections from mobile devices)
    New-NetFirewallRule -DisplayName "ShareJadPi - Inbound" `
                        -Direction Inbound `
                        -Program $exePath `
                        -Action Allow `
                        -Profile Private,Public `
                        -Protocol TCP `
                        -LocalPort 5000 `
                        -Description "Allow ShareJadPi to accept connections from mobile devices"
    
    Write-Host "✓ Inbound rule added (port 5000)" -ForegroundColor Green
    
    # Outbound rule (allows app to send data back)
    New-NetFirewallRule -DisplayName "ShareJadPi - Outbound" `
                        -Direction Outbound `
                        -Program $exePath `
                        -Action Allow `
                        -Profile Private,Public `
                        -Protocol TCP `
                        -Description "Allow ShareJadPi to send data to mobile devices"
    
    Write-Host "✓ Outbound rule added" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Firewall rules added!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Close ShareJadPi if it's running (right-click tray icon → Quit)" -ForegroundColor Yellow
    Write-Host "2. Run ShareJadPi-3.0.0.exe again" -ForegroundColor Yellow
    Write-Host "3. Right-click tray icon → Show QR" -ForegroundColor Yellow
    Write-Host "4. Scan QR with your mobile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Mobile should now connect successfully! 🎉" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to add firewall rules!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
pause
