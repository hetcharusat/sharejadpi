# ShareJadPi v3.0.0 - Production Release

## 🎉 Major Update: Live Zipping Progress & Performance Boost

ShareJadPi v3.0.0 brings significant performance improvements, reliability enhancements, and a much better user experience. This is the most stable and feature-complete version yet!

---

## 🚀 What's New

### ⚡ Performance Improvements
- **Background Folder Zipping** - No more UI freezing! Folders are now zipped in the background with live progress updates
- **10-20x Faster Zipping** - Switched to ZIP_STORED (no compression) for dramatically faster folder sharing
- **Live Progress with ETA** - See real-time zipping progress with percentage, speed (MB/s), and estimated time remaining
- **Memory-Safe Processing** - Streams files in 1MB chunks, preventing RAM spikes on large folders

### 🛡️ Reliability Enhancements
- **Robust File Deletion** - Retry logic with Windows reboot-delete fallback for locked files
- **No More Disk Leaks** - Proper file handle management ensures disk space fully recovers after clearing cache
- **Crash-Proof QR Generation** - Gracefully handles permission errors instead of crashing
- **ZIP64 Support** - Handle files larger than 2GB without issues

### 🎨 User Experience
- **Instant Mobile Loading** - Fixed the 40-50 second cache delay on mobile browsers
- **Aggressive Cache-Busting** - Always loads the latest version, no need to clear browser cache
- **Auto-Clear Service Workers** - Removes stale cached content automatically
- **Working Upload Speed Test** - Fixed the broken upload speed test (was only showing download)

### 🔧 Technical Improvements
- **Production Build System** - Automated build script for clean releases
- **Comprehensive Documentation** - Everything in one README with full guides
- **Error-Free Codebase** - All lint errors resolved, production-ready code

---

## 📥 Installation

### Option 1: Standalone Executable (Recommended)
1. Download `ShareJadPi-3.0.0.exe` below
2. Run the executable - that's it!
3. Scan the QR code with your phone
4. Start sharing files

### Option 2: Run from Source
```bash
git clone https://github.com/hetcharusat/sharejadpi.git
cd sharejadpi
pip install -r requirements.txt
python sharejadpi.py
```

---

## ✨ Key Features

- 🖱️ **Right-Click Sharing** - Share any file/folder from Windows Explorer
- 📱 **QR Code Access** - Instant mobile connection via QR code
- 🎨 **Beautiful Dark UI** - Modern gradient design with smooth animations
- 📤 **Drag & Drop Upload** - Upload files or entire folders from any device
- 📊 **Real-Time Progress** - Live upload/download speeds and progress bars
- 📋 **Shared Clipboard** - Sync text between devices automatically
- 🚄 **Network Speed Test** - Test your local network performance
- 📌 **Smart File Management** - Pin important files, auto-expiry for temporary shares
- 🔒 **Token Security** - Secure access with unique session tokens
- 💾 **Large File Support** - Handle files up to 50GB

---

## 🔄 Upgrade from v2.x

### Breaking Changes
None! v3.0.0 is fully compatible with v2.x. Just replace the old .exe with the new one.

### What Gets Better
- Folder uploads are 10-20x faster
- No more UI freezing on large folders
- Mobile browsers load instantly (no 40-50s delay)
- Disk space properly recovers after clearing cache
- Upload speed test now works correctly

---

## 🐛 Bug Fixes

- Fixed: Mobile browsers taking 40-50 seconds to load (aggressive caching)
- Fixed: Upload speed test not working (missing API endpoint)
- Fixed: Disk space not recovering after clear cache (file handle leaks)
- Fixed: App crashing on QR generation permission errors
- Fixed: Memory spikes when zipping large folders
- Fixed: Locked files preventing deletion after download

---

## 📋 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 2GB minimum, 4GB+ recommended for large files
- **Disk:** 100MB for app, plus space for shared files
- **Network:** WiFi or Ethernet connection

---

## 🔧 Technical Details

### Dependencies
- Python 3.8+
- Flask 3.0.0+
- qrcode[pil] 7.4.2+
- Pillow 10.0.0+
- pystray 0.19.5+

### Build Info
- **Version:** 3.0.0
- **Release Date:** October 15, 2025
- **Executable Size:** 35.44 MB
- **Build Tool:** PyInstaller
- **Python Version:** 3.13

---

## 📖 Documentation

Full documentation available in [README.md](https://github.com/hetcharusat/sharejadpi/blob/main/README.md):
- Quick Start Guide
- Usage Instructions
- Settings Configuration
- Troubleshooting
- Build Instructions

---

## 🙏 Acknowledgments

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [qrcode](https://github.com/lincolnloop/python-qrcode) - QR code generation
- [pystray](https://github.com/moses-palmer/pystray) - System tray icon

---

## 📄 License

MIT License - Free for personal and commercial use.

See [LICENSE](https://github.com/hetcharusat/sharejadpi/blob/main/LICENSE) for details.

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/hetcharusat/sharejadpi/issues)
- **Discussions:** [GitHub Discussions](https://github.com/hetcharusat/sharejadpi/discussions)

---

## 🎯 What's Next?

Planned for future releases:
- Multi-language support
- Dark/light theme toggle
- File preview before download
- Custom port configuration via UI
- Mobile app (Android/iOS)

---

**Full Changelog:** https://github.com/hetcharusat/sharejadpi/compare/v2.0.0...v3.0.0

Made with ❤️ for easy local file sharing
