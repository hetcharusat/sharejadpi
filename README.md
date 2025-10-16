# ShareJadPi v4.5.0

Share files ANYWHERE with one click — Local WiFi AND Public Internet.

[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/hetcharusat/sharejadpi)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

<div align="center">

### Download for Windows

<a href="https://github.com/hetcharusat/sharejadpi/releases/latest">
  <img src="https://custom-icon-badges.demolab.com/badge/-Download%20v4.5.0%20Setup-0078D4?style=for-the-badge&logo=download&logoColor=white&labelColor=1a1a1a" alt="Download ShareJadPi" width="400"/>
 </a>

<sub>Windows 10/11 (64‑bit) • One‑click installer • Firewall auto‑config</sub>

</div>

---

## ✨ Key Features

- 🖱️ One‑Click Sharing — Right‑click any file → “Share with ShareJadPi”
- 🔒 Token‑Based Security — 32‑char tokens protect access, no unauthorized use
- 📱 QR Code Access — Instant secure mobile connection (Local mode)
- ⚡ Background Folder Zipping — Live progress with speed & ETA
- 🌑 Beautiful Dark UI — Modern, responsive design
- � Clipboard Sync — Share text between devices
- 📶 Network Speed Test — Check your network performance
- 📦 Large File Support — Handle files up to 50GB
- � Multi‑Select Actions — Zip, pin, delete multiple files
- 🧰 System Tray App — Runs quietly in background; optional auto‑start

Online Share (UNIQUE): Send files over the public internet in ~10–15s with Cloudflare Tunnel — zero setup, no port forwarding, no DDNS, no VPN.

---

## Online Share (headline feature)

<div align="center">
  <img src="assets/vidss/context-menu-wit-online-share.png" width="420" alt="Context Menu – Share Online">
  <p><i>Right‑click any file/folder → “Share with ShareJadPi (Online)” → get a public https link.</i></p>
  <img src="assets/vidss/online-wait.png" width="420" alt="Waiting Page – Creating Tunnel">
  <p><i>Clean waiting page while the secure tunnel spins up.</i></p>
  <img src="assets/vidss/online-share-web-home.png" width="420" alt="Public Share Page">
  <p><i>The recipient gets a simple web page to download or upload (if enabled).</i></p>
</div>

---

## Screenshots

### Home Preview
<div align="center">
  <img src="assets/vidss/home-preview.jpg" width="320" alt="Home Preview">
</div>

### Shared Files Component
<div align="center">
  <img src="assets/vidss/shared-files-component.jpg" width="320" alt="Shared Files Component">
</div>

### Select Files and Zip
<div align="center">
  <img src="assets/vidss/select-files-and-zip.jpg" width="320" alt="Select Files and Zip">
</div>

### Uploading Files
<div align="center">
  <img src="assets/vidss/uploading-files.jpg" width="320" alt="Uploading Files">
</div>

### Zipping the Folder
<div align="center">
  <img src="assets/vidss/zipping-the-folder.png" width="320" alt="Zipping the Folder">
</div>

### Clipboard and Speed Test
<div align="center">
  <img src="assets/vidss/shared-clipboard-and-speedtest.jpg" width="320" alt="Shared Clipboard and Speed Test">
</div>

### Tray Icon Features
<div align="center">
  <img src="assets/vidss/tray-icon%20features.png" width="360" alt="Tray Icon Features">
</div>

---

## Quick Start

1) Download and run the v4.5.0 setup (above).
2) Right‑click a file/folder → “Share with ShareJadPi (Local/Online)”.
3) For Online Share, keep internet on; you’ll receive a public https link.

Run from source (optional):
```bash
git clone https://github.com/hetcharusat/sharejadpi.git
cd sharejadpi
pip install -r requirements.txt
python sharejadpi.py
```

For Online Share from source, place `cloudflared.exe` in the project root.

---

## Video demos (coming soon)

- ▶️ Context Menu Share (context-menu-share.mp4) — video placeholder
- ▶️ Open ShareJadPi (open_sharejadpi.mp4) — video placeholder
- ▶️ Settings Overview (settings.mp4) — video placeholder

Note: We’ll upload videos directly on GitHub for proper preview; links above are placeholders.

---

## Features

- 📦 Large files, folder zipping with progress
- 📱 QR code for quick mobile access (Local mode)
- 🔔 System tray app; optional auto‑start
- 📋 Clipboard sync and built‑in speed test
- 🌑 Modern dark UI, mobile‑friendly

---

## What’s New in v4.5.0

- Fixed crash in windowless EXE (stdout flush on None)
- Fixed “Verifying DNS propagation” infinite wait (now auto‑redirects)
- More robust `cloudflared.exe` path detection and timeouts

---

## Requirements

- Windows 10/11 (64‑bit)
- Python 3.8+ only if running from source

---

## License and Support

- MIT License — see `LICENSE`
- Issues and feature requests: GitHub Issues/Discussions

Made with ❤️ — Share locally. Share globally.
