# ShareJadPi v4.5.1 Release Notes

**Release Date:** January 2025  
**Version:** 4.5.1  
**Build Type:** Stable Release

---

## 🎯 Overview

ShareJadPi v4.5.1 is a **critical bug fix release** addressing persistent notification issues reported in v4.5.0. This update ensures Windows notifications are properly displayed across all Windows 10/11 systems and includes RAM optimization for improved performance.

---

## ✨ What's New

### 🔔 **Fixed: Windows Notifications Now Working Properly**
- **Root Cause Fixed:** Completely rewrote notification system to use proper Windows 10/11 toast API
- **New Library:** Integrated `winotify` for reliable Windows Action Center notifications
- **AppUserModelID Registration:** Proper Windows notification registration ensures toasts appear in Action Center
- **Quadruple Fallback System:**
  1. **Primary:** winotify (Windows 10/11 native toasts with AppUserModelID)
  2. **Fallback 1:** pystray balloon notification (system tray)
  3. **Fallback 2:** PowerShell toast with improved AppUserModelID
  4. **Fallback 3:** MessageBox (blocking but guaranteed visible)
- **Debug Logging:** Added comprehensive logging for troubleshooting notification issues

### 🚀 **RAM Optimization**
- Reduced `BASE_TIMEOUT_MINUTES` from 15 to 10 minutes for faster cloudflare tunnel cleanup
- More aggressive memory cleanup for online sharing sessions
- Improved background process management

### 🔧 **Technical Improvements**
- Added `APP_VERSION` constant for better version management
- Enhanced notification function with boolean return status
- Better icon path resolution for frozen vs script mode
- Improved error handling in notification delivery

---

## 🐛 Bug Fixes

| Issue | Description | Status |
|-------|-------------|--------|
| **Notifications Not Showing** | Windows toast notifications failed silently in v4.5.0 due to missing AppUserModelID registration | ✅ **FIXED** |
| **Silent Failures** | No feedback when notifications failed to display | ✅ **FIXED** with debug logging |
| **Online Share RAM Usage** | Cloudflare tunnels lingered too long after session end | ✅ **OPTIMIZED** |

---

## 📦 Dependencies Added

- **winotify** - Lightweight Windows notification library with proper toast support

---

## 🔄 Upgrade Notes

### For Users Upgrading from v4.5.0
- **Highly Recommended:** This is a critical bug fix for notification issues
- Download and run the v4.5.1 installer - it will automatically update your installation
- Notifications will now appear properly in Windows Action Center
- Online sharing sessions will clean up faster (10 min timeout vs 15 min)

### For Users on v4.1.x or Earlier
- All features from v4.5.0 are included:
  - ✅ Online sharing with cloudflared
  - ✅ Auto-reconnect for cloudflared
  - ✅ Enhanced error handling
  - ✅ Improved UI/UX
- Plus notification fixes and RAM optimization from v4.5.1

---

## 🎯 Key Features (All Versions)

1. **🌐 Online Sharing** - Share files globally with cloudflared tunnels (UNIQUE feature!)
2. **📱 QR Code Sharing** - Instant mobile device connections
3. **📋 Clipboard Sync** - Share text between devices
4. **📁 Context Menu Integration** - Right-click "Share with ShareJadPi" on any file/folder
5. **🖼️ System Tray App** - Persistent background service with tray icon
6. **⚡ Speed Test** - Built-in network speed testing
7. **🔔 Smart Notifications** - Now working reliably on all Windows versions!
8. **🔥 Firewall Auto-Config** - Automatic Windows firewall setup
9. **🎨 Modern Web UI** - Clean, responsive interface for file browsing
10. **🆓 Completely Free** - Open source with no subscription fees

---

## 📸 Screenshots

![Notification Working](../assets/vidss/notification-working.png)  
*Windows notifications now appear properly in Action Center*

---

## 🔗 Download

**Windows Installer:** [ShareJadPi-4.5.1-Setup.exe](https://github.com/hetp2/sharejadpi/releases/download/v4.5.1/ShareJadPi-4.5.1-Setup.exe)

**File Size:** ~35 MB  
**SHA256:** *[To be added after build]*

---

## 📝 Installation

1. Download `ShareJadPi-4.5.1-Setup.exe`
2. Run the installer (no admin rights required)
3. Choose installation options:
   - ✅ Add context menu integration (recommended)
   - ✅ Configure Windows firewall (recommended)
   - ⬜ Run at Windows startup (optional)
   - ⬜ Create desktop shortcut (optional)
4. Launch ShareJadPi from the system tray icon

---

## 🧪 Testing

### Notification Testing
- ✅ Verified winotify displays toasts in Windows 10/11 Action Center
- ✅ Tested fallback to pystray balloon notification
- ✅ Verified PowerShell fallback works on older systems
- ✅ Confirmed MessageBox emergency fallback never fails

### Online Sharing Testing
- ✅ Cloudflared tunnel startup and shutdown
- ✅ DNS propagation wait improvements
- ✅ Auto-reconnect functionality
- ✅ 10-minute timeout cleanup verification

---

## ⚠️ Known Issues

None at this time. All v4.5.0 issues have been resolved.

---

## 🛠️ Technical Details

### Build Information
- **Python Version:** 3.13.7
- **PyInstaller Version:** 6.16.0
- **Build Type:** Windows x64 standalone executable
- **New Dependencies:** winotify

### Notification System Architecture
```python
# Notification flow with fallbacks
1. Try winotify (Windows 10/11 native toast)
   ├─ Success → Return True
   └─ Fail → Try pystray balloon
       ├─ Success → Return True  
       └─ Fail → Try PowerShell toast
           ├─ Success → Return True
           └─ Fail → MessageBox (always succeeds)
```

---

## 🙏 Credits

- **Developer:** ShareJadPi Team
- **Contributors:** Community feedback and bug reports
- **Special Thanks:** Users who reported the notification issue in v4.5.0

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/hetp2/sharejadpi/issues)
- **Discussions:** [GitHub Discussions](https://github.com/hetp2/sharejadpi/discussions)
- **Documentation:** [README.md](../README.md)

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details

---

## 🔜 What's Next?

Stay tuned for future updates! Follow the repository for:
- 🎨 UI/UX improvements
- 🔐 Enhanced security features
- 📱 Mobile app companion
- 🌍 Multi-language support

---

**Download ShareJadPi v4.5.1 now and enjoy reliable notifications!** 🎉
