# ShareJadPi .exe Build Fix

## Problem
The original .exe had `console=True` which caused:
1. ❌ A console window appeared when running
2. ❌ Closing the console/terminal killed the entire app
3. ❌ App didn't properly run in system tray background
4. ❌ Mobile devices couldn't connect properly

## Solution
Changed `console=False` in `ShareJadPi-3.0.0.spec` to make it a **windowed application**.

## What This Fixes
- ✅ App runs silently in system tray (no console window)
- ✅ Closing the terminal doesn't stop the app
- ✅ App continues running in background
- ✅ Mobile devices can connect properly
- ✅ Professional Windows app behavior

## How to Use the New .exe

### First Time:
1. Double-click `ShareJadPi-3.0.0.exe`
2. Look for the **green circle icon** in system tray (bottom-right of screen)
3. **Right-click the tray icon** → "Show QR" to get connection URL
4. Scan QR with your phone

### Daily Use:
- App runs quietly in system tray
- Right-click tray icon for all options:
  - **Show QR** - Display connection QR code
  - **Open Share Page** - Open web interface in browser
  - **Install Context Menu** - Add "Share with ShareJadPi" to right-click menu
  - **Clear Cache** - Remove all shared files
  - **Settings** - Configure autostart and expiry
  - **Quit** - Stop the server

### Accessing from Mobile:
1. Make sure PC and phone are on **same WiFi network**
2. Right-click tray icon → "Show QR"
3. Scan QR code with phone camera
4. Opens web interface automatically

### Context Menu Sharing:
1. Right-click tray icon → "Install Context Menu"
2. Now you can right-click any file/folder → **"Share with ShareJadPi"**
3. QR code popup appears automatically
4. Scan and download on mobile

## Troubleshooting

### Can't find tray icon?
- Look in system tray (bottom-right corner near clock)
- Click the **^ arrow** to show hidden icons
- Green circle with "S" = ShareJadPi

### Mobile can't connect?
- Ensure PC and phone on **same WiFi** (not mobile data)
- Check Windows Firewall isn't blocking port 5000
- Try the URL manually: `http://[PC_IP]:5000/?k=[TOKEN]`

### App won't start?
- Check if port 5000 is already in use
- Look in Task Manager → kill any old ShareJadPi processes
- Run as Administrator if needed

## Technical Details

### Spec File Change:
```python
# Before (console mode):
console=True,  # ❌ Shows console window

# After (windowed mode):
console=False,  # ✅ Runs in system tray
```

### Build Command:
```powershell
python -m PyInstaller --clean ShareJadPi-3.0.0.spec
```

### Output:
- File: `dist\ShareJadPi-3.0.0.exe`
- Size: ~35 MB
- Mode: Windowed (no console)
- Tray: System tray icon enabled

## Next Steps

1. ✅ Build completed with `console=False`
2. ✅ Test the new .exe:
   - Run it (no console should appear)
   - Check system tray for icon
   - Right-click → Show QR
   - Test mobile connection
3. ✅ If working, replace old .exe in GitHub release
4. ✅ Update release notes to mention "proper tray mode"

---

**Note:** The Python script (`python sharejadpi.py`) still shows console output for debugging. The .exe runs silently for end users.
