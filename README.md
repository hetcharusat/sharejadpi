# ShareJadPi v4.0.0

**Fast, secure local file sharing between your PC and mobile devices over WiFi.**

[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/hetcharusat/sharejadpi)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

<div align="center">
  
### 📥 Download for Windows

<a href="https://github.com/hetcharusat/sharejadpi/releases/latest">
  <img src="https://custom-icon-badges.demolab.com/badge/-Download%20v4.0.0%20Setup-0078D4?style=for-the-badge&logo=download&logoColor=white&labelColor=1a1a1a&scale=2" alt="Download ShareJadPi" width="400"/>
</a>

**✨ One-click installer • 🔥 Firewall auto-configured • 🚀 Ready in 30 seconds**

<sub>Windows 10/11 (64-bit) • 20 MB download</sub>

</div>

---

ShareJadPi turns your Windows PC into a local file server accessible from any device on your network. Share files instantly, sync clipboard, upload from mobile, and more—all with a beautiful, modern web interface.

---
## ✨ Key Features

- 🖱️ **One-Click Sharing** - Right-click any file → "Share with ShareJadPi"
- 🔒 **Token-Based Security** - Unique 32-char tokens protect your files, no unauthorized access
- 📱 **QR Code Access** - Instant secure mobile connection
- ⚡ **Background Folder Zipping** - Live progress with speed & ETA
- 🎨 **Beautiful Dark UI** - Modern, responsive design
- 📋 **Clipboard Sync** - Share text between devices
- 🚀 **Network Speed Test** - Test local network performance
- 📦 **Large File Support** - Handle files up to 50GB
- 🔥 **Multi-Select Actions** - Zip, pin, delete multiple files
- ⚙️ **System Tray App** - Runs quietly in background

---

## 📸 Screenshots & Demo

### 🖱️ Context Menu Integration
Video: Coming soon — see the placeholders in [Video Tutorials](#-video-tutorials-placeholders)

### 🏠 Mobile Interface
<img src="assets/vidss/home-preview.jpg" width="280" alt="Home Preview">

### 📂 System Tray Access
Video: Coming soon — see the placeholders in [Video Tutorials](#-video-tutorials-placeholders)

### ☑️ Multi-Select & Zip
<img src="assets/vidss/select-files-and-zip.jpg" width="280" alt="Select and Zip">

### 📤 File Upload
<img src="assets/vidss/uploading-files.jpg" width="280" alt="Uploading">

### ⚙️ Settings Panel
Video: Coming soon — see the placeholders in [Video Tutorials](#-video-tutorials-placeholders)

### 📋 Clipboard & Speed Test
<img src="assets/vidss/shared-clipboard-and-speedtest.jpg" width="280" alt="Clipboard">

### 📁 File Management
<img src="assets/vidss/shared-files-component.jpg" width="280" alt="Files">

### 📦 Folder Zipping Progress
<img src="assets/vidss/zipping-the-folder.png" width="480" alt="Zipping">

---



## 🎯 Quick Start

### Download & Run (Recommended)
1. **Download** `ShareJadPi-4.0.0-Setup.exe` from [Releases](https://github.com/hetcharusat/sharejadpi/releases/latest)
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

- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to the project

---

## 🐛 Can't Connect from Mobile?

**#1 Issue:** Missed the firewall prompt!

**Quick Fix:**
1. Download and run the installer - it configures firewall automatically
2. Or manually allow port 5000 in Windows Firewall
3. Restart ShareJadPi

---

## 🚀 What's New in v4.0

- 🔒 Stronger security: token-gated routes, Cloudflare header detection, remote settings hidden
- 📱 Smarter QR and notifications: separate local vs tunnel QR; multi-line Windows toasts
- 🚧 More reliable online sharing: server-side reachability check before redirect; improved waiting page (dark theme)
- ⏱️ Dynamic idle timeout based on file size with activity tracking during downloads
- 📣 Clearer Windows notifications during context menu actions

---

## 🎬 Video Tutorials (placeholders)

We’ll publish short video tutorials soon. Until then, these placeholders indicate what’s coming:

- ▶️ Installation & Setup: https://youtu.be/PLACEHOLDER_INSTALL
- ▶️ Share Locally (Context Menu): https://youtu.be/PLACEHOLDER_LOCAL_SHARE
- ▶️ Share Online (Cloudflare Tunnel): https://youtu.be/PLACEHOLDER_ONLINE_SHARE
- ▶️ Fix Windows Firewall for Mobile Access: https://youtu.be/PLACEHOLDER_FIREWALL
- ▶️ QR Code & Mobile Access: https://youtu.be/PLACEHOLDER_QR
- ▶️ Troubleshooting (Common Issues): https://youtu.be/PLACEHOLDER_TROUBLESHOOT

For a full list, see docs/VIDEOS.md (to be updated with real links once published).

---

## 📋 Requirements

- Windows 10/11 (64-bit)
- Python 3.8+ (if running from source)
- WiFi or Ethernet
- 100MB disk space + file storage

---

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for development setup and guidelines.

Fork → Branch → Commit → Push → PR — Welcome! 🎉

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 💬 Support

- [Issues](https://github.com/hetcharusat/sharejadpi/issues)
- [Discussions](https://github.com/hetcharusat/sharejadpi/discussions)

---

Made with ❤️ for easy local file sharing
