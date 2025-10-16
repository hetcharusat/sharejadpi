# ShareJadPi v3.0.0

**Fast, secure local file sharing between your PC and mobile devices over WiFi.**

[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/hetcharusat/sharejadpi)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

<div align="center">

## 📥 Download ShareJadPi

<a href="https://github.com/hetcharusat/sharejadpi/releases/download/setup-3.1/ShareJadPi-3.1.1-Setup.exe">
  <img src="https://img.shields.io/badge/Download-ShareJadPi%20v3.1.1%20Setup-blue?style=for-the-badge&logo=windows&logoColor=white" alt="Download ShareJadPi v3.1.1">
</a>

**✨ One-click installer • 🔥 Firewall auto-config • 🚀 Ready in seconds**

</div>

---

ShareJadPi turns your Windows PC into a local file server accessible from any device on your network. Share files instantly, sync clipboard, upload from mobile, and more—all with a beautiful, modern web interface.

---
## ✨ Key Features

- 🖱️ **One-Click Sharing** - Right-click any file → "Share with ShareJadPi"
- � **Token-Based Security** - Unique 32-char tokens protect your files, no unauthorized access
- 📱 **QR Code Access** - Instant secure mobile connection
- ⚡ **Background Folder Zipping** - Live progress with speed & ETA
- 🎨 **Beautiful Dark UI** - Modern, responsive design
- 📋 **Clipboard Sync** - Share text between devices
- 🚀 **Network Speed Test** - Test local network performance
- � **Large File Support** - Handle files up to 50GB
- 🔥 **Multi-Select Actions** - Zip, pin, delete multiple files
- ⚙️ **System Tray App** - Runs quietly in background

---

## 📸 Screenshots & Demo

### 🖱️ Context Menu Integration
https://github.com/user-attachments/assets/46c6b784-f82c-40e3-9c21-6bab15435278

### 🏠 Mobile Interface
<img src="vidss/home-preview.jpg" width="280" alt="Home Preview">

### 📂 System Tray Access
https://github.com/user-attachments/assets/d1145397-81a6-4531-b606-34caf9a6c9b2

### ☑️ Multi-Select & Zip
<img src="vidss/select-files-and-zip.jpg" width="280" alt="Select and Zip">

### 📤 File Upload
<img src="vidss/uploading-files.jpg" width="280" alt="Uploading">

### ⚙️ Settings Panel
https://github.com/user-attachments/assets/fb9ed56a-fc1f-459b-abb0-86ee14cc620b

### 📋 Clipboard & Speed Test
<img src="vidss/shared-clipboard-and-speedtest.jpg" width="280" alt="Clipboard">

### 📁 File Management
<img src="vidss/shared-files-component.jpg" width="280" alt="Files">

### 📦 Folder Zipping Progress
<img src="vidss/zipping-the-folder.png" width="480" alt="Zipping">

---



## 🎯 Quick Start

### Download & Run (Recommended)
1. **Download** `ShareJadPi-3.0.0.exe` from [Releases](https://github.com/hetcharusat/sharejadpi/releases)
2. **Run** the exe
3. **Allow firewall** when prompted ⚠️ *Important: Don't miss this!*
4. **Right-click tray icon** → "Show QR"
5. **Scan QR** with your phone → Done! 🎉

### Run from Source
```bash
git clone https://github.com/hetcharusat/sharejadpi.git
cd sharejadpi
pip install -r requirements.txt
python sharejadpi.py
```

---

## 📖 Documentation

- **[Usage Guide](USAGE_GUIDE.md)** - How to use all features
- **[Troubleshooting](TROUBLESHOOTING.md)** - Fix common issues
- **[Build Guide](BUILD_SUMMARY.md)** - Build your own .exe
- **[Release Notes](RELEASE_NOTES_v3.md)** - What's new

---

## 🐛 Can't Connect from Mobile?

**#1 Issue:** Missed the firewall prompt!

**Quick Fix:**
1. Right-click `fix_firewall.ps1` → "Run as Administrator"
2. Quit ShareJadPi (tray icon → Quit)
3. Run ShareJadPi again
4. Try mobile

More help: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🚀 What's New in v3.0

- ⚡ Background folder zipping with live progress
- 🚄 10-20x faster zipping (no compression)
- 💾 Memory-safe streaming for large files
- 🔧 Robust file deletion with Windows API
- 🎨 Aggressive cache-busting for mobile
- 🔼 Fixed network speed test

---

## 📋 Requirements

- Windows 10/11 (64-bit)
- Python 3.8+ (if running from source)
- WiFi or Ethernet
- 100MB disk space + file storage

---

## 🤝 Contributing

Fork → Branch → Commit → Push → PR 

Welcome! 🎉

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 💬 Support

- [Issues](https://github.com/hetcharusat/sharejadpi/issues)
- [Discussions](https://github.com/hetcharusat/sharejadpi/discussions)

---

Made with ❤️ for easy local file sharing
