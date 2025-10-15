# ShareJadPi - Show Correct Connection URL
# This helps when you have multiple network adapters

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ShareJadPi - Connection Info" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get all network IPs
$ips = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"}

Write-Host "Your PC's Network Addresses:" -ForegroundColor Yellow
Write-Host ""

foreach ($ip in $ips) {
    $adapter = Get-NetAdapter -InterfaceIndex $ip.InterfaceIndex -ErrorAction SilentlyContinue
    $status = if ($adapter.Status -eq "Up") { "[ACTIVE]" } else { "[Inactive]" }
    $color = if ($adapter.Status -eq "Up") { "Green" } else { "Gray" }
    
    Write-Host "  $($ip.IPAddress)" -NoNewline -ForegroundColor White
    Write-Host " [$($ip.InterfaceAlias)]" -NoNewline -ForegroundColor Cyan
    Write-Host " - $status" -ForegroundColor $color
    
    # Check if this is likely the WiFi/Ethernet adapter
    if ($adapter.Status -eq "Up" -and $ip.InterfaceAlias -match "Wi-Fi|Ethernet|WLAN" -and $ip.InterfaceAlias -notmatch "VirtualBox|VMware|Hyper-V|vEthernet") {
        Write-Host "    >> Use this one for mobile connection!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Connection URL:" -ForegroundColor Yellow
Write-Host ""

# Get the primary WiFi/Ethernet IP (not VirtualBox)
$mainIP = $ips | Where-Object { 
    $adapter = Get-NetAdapter -InterfaceIndex $_.InterfaceIndex -ErrorAction SilentlyContinue
    $adapter.Status -eq "Up" -and 
    $_.InterfaceAlias -match "Wi-Fi|Ethernet|WLAN" -and 
    $_.InterfaceAlias -notmatch "VirtualBox|VMware|Hyper-V|vEthernet"
} | Select-Object -First 1

if ($mainIP) {
    Write-Host "Your mobile should use:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  http://$($mainIP.IPAddress):5000/?k=YOUR_TOKEN" -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host ""
    Write-Host "Replace YOUR_TOKEN with the token from ShareJadPi QR code" -ForegroundColor Gray
} else {
    Write-Host "No active WiFi/Ethernet adapter found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Troubleshooting:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Make sure mobile is on same WiFi as PC" -ForegroundColor White
Write-Host "2. Right-click ShareJadPi tray icon → Show QR" -ForegroundColor White
Write-Host "3. Check the QR shows: http://192.168.0.100:5000/..." -ForegroundColor White
Write-Host "4. Scan QR with mobile camera" -ForegroundColor White
Write-Host ""
Write-Host "If QR shows 192.168.56.1 instead:" -ForegroundColor Yellow
Write-Host "  - That is the VirtualBox network (wrong one!)" -ForegroundColor Red
Write-Host "  - ShareJadPi might be using the wrong adapter" -ForegroundColor Red
Write-Host ""

pause
