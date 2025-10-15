# ShareJadPi Troubleshooting Guide

## Mobile Can't Connect ("Site Can't Be Reached")

This is the most common issue. Follow these steps:

### Quick Fix (Run This First!)

1. **Right-click** `fix_firewall.ps1`
2. Select **"Run with PowerShell (Admin)"**
3. Press any key when it finishes
4. **Close ShareJadPi** (right-click tray icon → Quit)
5. **Run ShareJadPi** again
6. Try connecting from mobile

---

## Manual Troubleshooting

### Step 1: Check WiFi Connection

**Both PC and mobile MUST be on the same WiFi network!**

- ✅ PC WiFi: Check your PC's WiFi name
- ✅ Mobile WiFi: Open mobile WiFi settings and verify it matches
- ❌ Mobile Data: Turn OFF mobile data, use WiFi only

### Step 2: Verify ShareJadPi is Running

1. Look for **green circle icon** in system tray (bottom-right)
2. If not visible, click the **^ arrow** to show hidden icons
3. If no icon, ShareJadPi isn't running - double-click the `.exe` file

### Step 3: Check Windows Firewall

**Problem:** When you first run ShareJadPi, Windows shows a network access prompt. If you click "Cancel" or close it, Windows blocks all connections.

**Solution:**

1. Run `fix_firewall.ps1` as Administrator (see Quick Fix above)
2. OR manually add firewall rule:
   - Open Windows Defender Firewall
   - Advanced Settings
   - Inbound Rules → New Rule
   - Port → TCP → 5000 → Allow
   - Apply to all profiles
   - Name it "ShareJadPi"

### Step 4: Test Connection

1. **On your PC browser**, go to: `http://192.168.1.11:5000/`
   - ✅ If it works: Problem is between PC and mobile
   - ❌ If it doesn't work: Problem is with ShareJadPi itself

2. **Check your PC's IP address:**
   - Run `show_connection_info.ps1`
   - Look for the WiFi IP (usually starts with `192.168.`)
   - Your mobile needs this exact IP

3. **On your mobile browser**, type:
   ```
   http://[YOUR_PC_IP]:5000/
   ```
   Replace `[YOUR_PC_IP]` with the IP from step 2

### Step 5: Check Network Type

Windows treats networks differently:

- ✅ **Private Network**: Allows local connections (CORRECT)
- ❌ **Public Network**: Blocks local connections (WRONG)

**To change:**

1. Open Settings → Network & Internet
2. Click your WiFi network
3. Under "Network profile type", select **Private**

---

## Common Issues

### Issue: "Mobile keeps loading forever"

**Cause:** Windows Firewall is blocking port 5000

**Fix:** Run `fix_firewall.ps1` as Administrator

---

### Issue: "QR code shows wrong IP (192.168.56.1)"

**Cause:** You have VirtualBox/VMware installed, creating virtual networks

**Fix:** 
1. The app should auto-detect the correct WiFi IP
2. If not, manually type the correct IP in mobile browser
3. Check WiFi IP using: `ipconfig | findstr "IPv4"`

---

### Issue: "Multiple ShareJadPi icons in tray"

**Cause:** App was started multiple times

**Fix:**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find all "ShareJadPi" processes
3. End all of them
4. Run ShareJadPi once

---

### Issue: "Port 5000 already in use"

**Cause:** Another app is using port 5000

**Fix:**
1. Find what's using port 5000:
   ```powershell
   netstat -ano | findstr :5000
   ```
2. Find the process ID (rightmost number)
3. Open Task Manager → Details tab
4. Find process by ID and end it
5. Run ShareJadPi again

---

### Issue: "Mobile connected before, now doesn't work"

**Possible causes:**
- PC's IP address changed (router assigns new IPs)
- PC/Mobile switched WiFi networks
- Windows Firewall was reset/updated

**Fix:**
1. Right-click tray icon → Show QR
2. Get the NEW QR code (IP may have changed)
3. Scan fresh QR code from mobile

---

## Advanced Troubleshooting

### Test if port 5000 is accessible:

```powershell
Test-NetConnection -ComputerName localhost -Port 5000
```

Should show `TcpTestSucceeded : True`

### Check firewall rules:

```powershell
Get-NetFirewallRule -DisplayName "*ShareJadPi*" | Select-Object DisplayName, Enabled, Direction, Action
```

Should show at least one rule with:
- `Direction: Inbound`
- `Action: Allow`
- `Enabled: True`

### View all network IPs:

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*"} | Select-Object IPAddress, InterfaceAlias
```

Look for the one labeled "Wi-Fi" or "Ethernet"

---

## Still Not Working?

### Temporary Workaround:

Disable Windows Firewall temporarily to test:

1. Open Windows Security
2. Firewall & network protection
3. Turn OFF for Private networks
4. Test mobile connection
5. **IMPORTANT:** Turn firewall back ON after testing!

If it works with firewall off, the issue is definitely firewall rules.

### Last Resort - Network Reset:

If nothing works:

1. Close ShareJadPi completely
2. Restart your router
3. Restart your PC
4. Reconnect both PC and mobile to WiFi
5. Run `fix_firewall.ps1` again
6. Start ShareJadPi

---

## For Users Without PowerShell Knowledge

If your users can't run PowerShell scripts:

### Alternative Fix Method:

1. **Open Windows Defender Firewall with Advanced Security**
   - Press Windows key
   - Type "Windows Defender Firewall with Advanced Security"
   - Click it

2. **Add Inbound Rule:**
   - Click "Inbound Rules" on the left
   - Click "New Rule" on the right
   - Select "Port" → Next
   - Select "TCP" and type "5000" → Next
   - Select "Allow the connection" → Next
   - Check all boxes (Domain, Private, Public) → Next
   - Name: "ShareJadPi" → Finish

3. **Test again** from mobile

---

## Prevention

To avoid this issue in the future:

1. **Always click "Allow"** when Windows shows network prompt
2. **Keep `fix_firewall.ps1`** handy for quick fixes
3. **Set WiFi to Private network** not Public
4. **Use static IP** if your router supports it (prevents IP changes)

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Mobile can't connect | Run `fix_firewall.ps1` as Admin |
| Wrong IP in QR | Manually type WiFi IP in mobile browser |
| Multiple instances running | Task Manager → End all ShareJadPi processes |
| Port already in use | Find and close app using port 5000 |
| IP changed | Get new QR code from tray icon |

---

**Note:** ShareJadPi works 100% locally - no internet required. PC and mobile just need to be on the same WiFi network!
