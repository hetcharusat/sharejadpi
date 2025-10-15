# ShareJadPi Installer Guide

## For End Users (Installing ShareJadPi)

### Easy Installation

1. **Download** `ShareJadPi-3.0.0-Setup.exe` from [Releases](https://github.com/hetcharusat/sharejadpi/releases)

2. **Run the installer** (double-click the Setup.exe)

3. **Accept UAC prompt** (required for firewall configuration)

4. **Choose installation options:**
   - ✅ **Add Windows Firewall rule** - REQUIRED for mobile access (recommended)
   - ✅ **Add to right-click menu** - Share files easily (recommended)
   - ✅ **Start with Windows** - Auto-start on boot (optional)
   - ☐ **Desktop shortcut** - Quick access icon (optional)

5. **Click Install** and wait ~30 seconds

6. **Done!** ShareJadPi starts automatically with green tray icon

### What Gets Installed

**Program Files:**
- Main application: `ShareJadPi-3.0.0.exe`
- Documentation: README, Troubleshooting Guide, Release Notes
- Helper scripts: Firewall fix, Connection info

**Start Menu Items:**
- ShareJadPi (launch app)
- Troubleshooting Guide
- Fix Firewall (if connection issues)
- Show Connection Info
- Uninstall

**Registry Entries:**
- Context menu: Right-click → "Share with ShareJadPi"
- Autostart: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

**Firewall Rules:**
- Allows incoming connections on port 5000 (TCP)
- Required for mobile device access

### First Run

After installation:

1. **Look for green tray icon** (bottom-right corner)
2. **Right-click icon** → **"Show QR"**
3. **Scan QR with mobile** to access web interface
4. **Done!** Start sharing files

### Uninstallation

**Easy way:**
- Start Menu → ShareJadPi → Uninstall

**Alternative:**
- Settings → Apps → ShareJadPi → Uninstall

**What gets removed:**
- Application files
- Context menu integration
- Autostart entry
- Firewall rules
- Start Menu shortcuts

**What stays:**
- Your shared files in `%LOCALAPPDATA%\ShareJadPi\`
- (Delete manually if you want to remove all data)

---

## For Developers (Building the Installer)

### Prerequisites

1. **Inno Setup 6** (free, open-source)
   - Download: https://jrsoftware.org/isdl.php
   - Install with default options

2. **Built ShareJadPi executable**
   - Must have `dist\ShareJadPi-3.0.0.exe` ready
   - Build with: `.\build_v3.ps1`

### Build Steps

1. **Ensure exe is built:**
   ```powershell
   .\build_v3.ps1
   ```

2. **Run installer build script:**
   ```powershell
   .\build_installer.ps1
   ```

3. **Output location:**
   ```
   installer_output\ShareJadPi-3.0.0-Setup.exe
   ```

### Manual Build (Optional)

If you prefer to build manually:

1. Open **Inno Setup Compiler**
2. File → Open → `ShareJadPi-Installer.iss`
3. Build → Compile
4. Find output in `installer_output\`

### Installer Features

**Automatic Configuration:**
- ✅ Detects if app is running (kills gracefully)
- ✅ Adds firewall rule via `netsh` (no user prompts)
- ✅ Integrates context menu seamlessly
- ✅ Sets up autostart if selected
- ✅ Creates uninstaller automatically

**User Experience:**
- Modern wizard UI
- Custom post-install message with tips
- Progress indicators
- Rollback on error
- Silent install support: `/SILENT` or `/VERYSILENT`

### Customization

Edit `ShareJadPi-Installer.iss` to customize:

**Branding:**
```pascal
#define MyAppName "ShareJadPi"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "hetcharusat"
```

**Installation Directory:**
```pascal
DefaultDirName={autopf}\{#MyAppName}
```

**Default Tasks:**
- `checkedonce` - Checked by default, remember user choice
- `unchecked` - Not checked by default

**Add Custom Files:**
```pascal
[Files]
Source: "path\to\file.txt"; DestDir: "{app}"; Flags: ignoreversion
```

**Add Custom Registry Keys:**
```pascal
[Registry]
Root: HKLM; Subkey: "Software\MyApp"; ValueType: string; ValueName: "Path"; ValueData: "{app}"
```

### Silent Installation

For automated deployments:

```powershell
# Silent install with all features
ShareJadPi-3.0.0-Setup.exe /VERYSILENT /TASKS="firewall,contextmenu,autostart"

# Silent install, firewall only
ShareJadPi-3.0.0-Setup.exe /VERYSILENT /TASKS="firewall"

# Silent uninstall
unins000.exe /VERYSILENT
```

### Testing

**Test installer:**
1. Build installer
2. Install on a clean VM or test PC
3. Verify all features work:
   - App starts and shows tray icon
   - Right-click menu appears
   - Firewall allows connections
   - Mobile can connect
   - Autostart works after reboot
4. Test uninstall (everything should be removed)

**Test upgrade:**
1. Install older version
2. Install new version over it
3. Should upgrade smoothly without conflicts

---

## Comparison: Installer vs Standalone .exe

### Installer (ShareJadPi-3.0.0-Setup.exe)

**Pros:**
- ✅ Automatic firewall configuration (no manual steps)
- ✅ Context menu integration (optional)
- ✅ Autostart setup (optional)
- ✅ Start Menu shortcuts
- ✅ Professional uninstaller
- ✅ Perfect for non-technical users
- ✅ One-click setup

**Cons:**
- ❌ Requires administrator rights
- ❌ Slightly larger download (~40 MB vs 35 MB)
- ❌ Installs to Program Files (not portable)

**Best for:**
- End users
- Permanent installations
- Corporate deployments
- People who want "it just works"

---

### Standalone .exe (ShareJadPi-3.0.0.exe)

**Pros:**
- ✅ Portable (run from USB, Downloads, anywhere)
- ✅ No installation required
- ✅ No administrator rights needed (except firewall)
- ✅ Smaller download
- ✅ Perfect for testing

**Cons:**
- ❌ Manual firewall setup (run fix_firewall.ps1)
- ❌ Manual context menu setup
- ❌ No uninstaller (just delete file)
- ❌ Requires running fix_firewall.ps1 separately

**Best for:**
- Developers/tech-savvy users
- Portable/USB installations
- Testing/temporary use
- Users who don't want "install" commitment

---

## Recommendation

**For GitHub Releases, provide BOTH:**

1. **ShareJadPi-3.0.0-Setup.exe** (Installer)
   - Recommended for most users
   - "Install and forget" experience

2. **ShareJadPi-3.0.0.exe** (Standalone)
   - For advanced users
   - Portable option

**Release Notes Template:**

```markdown
## Download Options

### 🎯 Recommended: Installer (for most users)
**ShareJadPi-3.0.0-Setup.exe** (40 MB)
- One-click installation
- Automatic firewall setup
- Context menu integration
- Starts with Windows (optional)
- Professional uninstaller

### 💼 Advanced: Standalone Executable
**ShareJadPi-3.0.0.exe** (35 MB)
- Portable (no installation)
- Run from anywhere
- Requires manual firewall setup: Run `fix_firewall.ps1` as Admin
- Perfect for USB drives or testing
```

---

## Troubleshooting Installer Issues

### "Windows protected your PC" SmartScreen warning

**Why:** Unsigned installer (code signing costs $$$)

**Fix:**
- Click "More info"
- Click "Run anyway"
- Or sign the installer with a code signing certificate

### Installer won't run / Access denied

**Fix:**
- Right-click Setup.exe → "Run as administrator"

### Firewall rule not added

**Fix:**
- Manually run: `fix_firewall.ps1` as Administrator
- Or manually add port 5000 to Windows Firewall

### Context menu not appearing after install

**Fix:**
- Restart Windows Explorer: Press Ctrl+Shift+Esc → Find "Windows Explorer" → Restart
- Or log out and log back in

### Uninstall leaves files behind

**Expected behavior:**
- User data in `%LOCALAPPDATA%\ShareJadPi\` is preserved
- To remove completely: Delete that folder manually

---

## Future Enhancements

Ideas for future versions:

- [ ] Code signing certificate (removes SmartScreen warnings)
- [ ] Auto-updater (check for new versions)
- [ ] Multiple language support
- [ ] Custom installation directory picker
- [ ] Portable mode toggle (in installer)
- [ ] Import/export settings during upgrade
- [ ] MSI installer for enterprise deployment

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub!
