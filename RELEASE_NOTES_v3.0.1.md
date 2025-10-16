# ShareJadPi v3.0.1 - Bug Fix Release

**Release Date:** October 16, 2025

## 🐛 Bug Fix

### Fixed: "ValueError: read of closed file" Error

**Issue:** When downloading multiple files as a ZIP (Select Multiple → Zip & Download), the download would fail with:
```
ValueError: read of closed file
```

**Root Cause:** File handles were being closed prematurely by Python's context manager (`with open()`) before Flask finished streaming the file to the browser.

**Fix:** Changed file serving to let Flask handle the entire file lifecycle (open, stream, close) by passing file paths directly instead of file objects.

**Impact:** 
- ✅ Multi-select ZIP downloads now work perfectly
- ✅ Single file downloads are more reliable
- ✅ No more file handle leaks

---

## 📥 Download

### 🎯 Recommended: Installer (for most users)
**ShareJadPi-3.0.1-Setup.exe** (~40 MB)
- ✅ One-click installation
- ✅ Automatic Windows Firewall setup
- ✅ Context menu integration (optional)
- ✅ Autostart with Windows (optional)
- ✅ Professional uninstaller

### 💼 Advanced: Standalone Portable
**ShareJadPi-3.0.1.exe** (~35 MB)
- ✅ No installation required
- ✅ Run from USB or Downloads folder
- ⚠️ Requires manual firewall setup (run `fix_firewall.ps1` as Admin)
- ✅ Perfect for portable use

---

## 🔧 Requirements

- Windows 10/11 (64-bit)
- Same WiFi network for PC and mobile
- ~100MB disk space

---

## 📝 Changelog

### Changed
- Fixed file download streaming issue (no more "read of closed file" errors)
- Improved file handle management in download routes

---

## ⚠️ Upgrade from v3.0.0

If you installed v3.0.0:

**Installer Version:**
1. Download new installer
2. Run it (will upgrade automatically)
3. Done!

**Portable Version:**
1. Close old ShareJadPi-3.0.0.exe
2. Download new ShareJadPi-3.0.1.exe
3. Run the new version
4. Delete old exe (optional)

Your settings and shared files are preserved (stored in `%LOCALAPPDATA%\ShareJadPi\`).

---

## 🎉 What's Still Awesome in v3.0.x

- System tray mode (no console window)
- Background folder zipping with live progress
- Robust file cleanup (never leaves orphaned files)
- Cache-busting for instant UI updates
- Professional Windows installer
- Automatic firewall configuration

---

**Full v3.0.0 Features:** See [RELEASE_NOTES_v3.md](RELEASE_NOTES_v3.md)

**Need Help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
