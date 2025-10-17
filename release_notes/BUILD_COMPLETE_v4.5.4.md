# BUILD COMPLETE — ShareJadPi v4.5.4

Date: 2025-10-17

Artifacts to publish:
- Installer: installer_output/ShareJadPi-4.5.4-Setup.exe
- Portable EXE: dist/ShareJadPi-4.5.4.exe
- Release Notes: release_notes/RELEASE_NOTES_v4.5.4.md

Key differences vs 4.5.3:
- Token hidden in URL via POST `/auth/enter`
- Reachability check via `GET /health` through tunnel
- Double-token bug fixed
- 2‑minute server+client caches for same-host tunnel reuse
- DoH used for status messaging only

Manual checklist:
1. Verify `sharejadpi.py` APP_VERSION = 4.5.4
2. Build EXE with PyInstaller spec 4.5.4
3. Build installer with Inno Setup 4.5.4
4. Smoke test: Local share, Online share wait/redirect, tokenless URL, re-open speed
5. Publish on GitHub Releases with notes
