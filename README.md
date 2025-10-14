## Overview

ShareJadPi lets you share files on your local Wi‑Fi with zero setup. It has a modern UI, a Windows tray icon, and a right‑click Explorer menu for instant sharing. Built by [@hetpatel7567](https://github.com/hetpatel7567).

> Image placeholders (add later):
> - ![Home UI](docs/images/home.png)
> - ![Shared Clipboard](docs/images/clipboard.png)
> - ![Speed Test](docs/images/speedtest.png)

## Features

- QR code to connect from phone; mobile-friendly UI
- Right‑click → Share with ShareJadPi (files/folders), with auto‑generated QR
- Multi‑use shares (copies/zips) and single‑use uploads
- Shared clipboard across devices (in-memory), plus “clip to .txt file”
- 5‑second combined up/download speed test with live Mbps and progress
- Auto‑start, tray icon (Open, Show QR, Install/Remove Context Menu, Clear Cache, Settings)
- Automatic expiry and cache management

## Download (Users)

- Download the single EXE from Releases (or `dist/ShareJadPi.exe` after you build).
- Double‑click to run → opens http://127.0.0.1:5000 and installs the context menu (per-user).
- Right‑click any file/folder → Share with ShareJadPi.

## Multi‑use vs Single‑use

- Multi‑use: created when you share existing files/folders (right‑click or CLI). Stays until deleted or expired.
- Single‑use: created via website uploads or the “clip to file” endpoint. Deleted after the first real download.

## Build (Maintainers)

Prereqs: Windows + Python 3.11+.

1) Install
```powershell
pip install -r requirements.txt pyinstaller
```

2) Build
```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

Output: `dist\ShareJadPi.exe`

Optional flags: `-Icon path.ico`, `-OneDir`, `-Debug`, `-Python .\.venv\Scripts\python.exe`

## Context Menu (built-in)

The EXE installs the context menu for the current user on first run. You can manage it via:

- Tray menu: Install Context Menu / Remove Context Menu
- CLI: `ShareJadPi.exe install-context-menu` or `ShareJadPi.exe uninstall-context-menu`

## Data Folders

`%LOCALAPPDATA%\ShareJadPi`
- `shared\` — multi‑use copies/zips
- `uploads\` — single‑use uploads and clip files

## Troubleshooting

- If the context menu doesn’t appear, run the EXE once (first‑run installs it) or use the tray to install it.
- If Windows Firewall prompts, allow Private networks so your phone can reach your PC.
- On corporate machines, registry policy might block HKCU writes; the app still works without the menu.

## License

MIT © [hetpatel7567](https://github.com/hetpatel7567)
