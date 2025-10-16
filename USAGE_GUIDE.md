# ShareJadPi Usage Guide

## 📖 First Time Setup

1. **Start the app** (exe or `python sharejadpi.py`)
2. **Look for the system tray icon** (green circle with 'S')
3. **Right-click tray icon** → "Show QR" to get the access URL
4. **Scan QR with your phone** to open the web interface

---

## 📤 Sharing Files

### Method 1: Context Menu (Fastest)
- Right-click any file or folder
- Select **"Share with ShareJadPi"**
- QR code pops up automatically
- Scan and download on mobile

### Method 2: Direct Upload from Mobile
- Open web interface on any device
- Drag & drop files or folders
- Or click "Choose Files" / "Choose Folder"
- See live upload progress

---

## 📁 Managing Files

### Download Files
- Click any file to download directly
- Files stream efficiently (no size limits up to 50GB)

### Multi-Select Actions
Check boxes to select multiple files, then:
- **Zip Selected** - Download multiple files as one zip
- **Pin** - Prevent auto-expiry (⭐ icon appears)
- **Delete** - Remove selected files

### Individual File Actions
- **Pin** - Click ⭐ to keep files from auto-expiring
- **Delete** - Click 🗑️ to remove immediately
- **Clear All** - Remove all shared files at once (in header)

---

## 📋 Clipboard Sync

Share text between your PC and mobile:

1. Open web interface on mobile
2. Scroll to "Shared Clipboard" section
3. Type text and click **Save**
4. Text syncs automatically across all devices (updates every 2 seconds)
5. Click **Clear** to remove

**Use cases:**
- Copy URLs from PC to phone
- Share notes between devices
- Transfer code snippets quickly

---

## 🚀 Network Speed Test

Test your local network performance:

1. Click **"🚀 Run Speed Test (5 seconds)"**
2. See real-time download & upload speeds
3. Helps diagnose connection issues

**What it tests:**
- Download speed (PC → Mobile)
- Upload speed (Mobile → PC)
- Network latency

---

## ⚙️ Settings (Host PC Only)

Access settings at `http://127.0.0.1:5000/settings` (only works on the PC running ShareJadPi)

### Autostart
- ✅ **Enable** - Start ShareJadPi automatically when Windows starts
- ❌ **Disable** - Start manually

### File Expiry
- Set minutes before files auto-delete (default: 60 minutes)
- Set to `0` to never expire files
- Pinned files (⭐) never expire regardless of this setting
- Useful for temporary shares that clean up automatically

### Context Menu Integration
- **Install** - Add "Share with ShareJadPi" to Windows right-click menu
- **Uninstall** - Remove context menu integration
- Requires Explorer restart to take effect

### Cache Management
- View disk usage:
  - Shared files (from PC)
  - Uploaded files (from mobile)
  - Registry/settings
- **Clear All** - Remove all files and reset storage

---

## 🔐 Security Features

### Token-Based Authentication
- Every session has a unique 32-character token
- Token is included in the QR code URL automatically
- Cookies stored for 7 days after first scan
- Without valid token, files are not accessible

### Host-Only Features
- Settings page only accessible from the PC running ShareJadPi
- Context menu and autostart management restricted to host
- Prevents remote configuration changes

### Network Isolation
- Only accessible on your local network (LAN/WiFi)
- Not exposed to the internet
- No port forwarding or external access

---

## 🎨 Interface Tips

### Mobile Interface
- **Responsive design** - Works on any phone size
- **Dark theme** - Easy on eyes with gradient design
- **Touch gestures** - Swipe-friendly controls
- **Live updates** - Progress bars show real-time speed

### Desktop Interface
- **System tray control** - All features from tray icon
- **QR code generator** - Quick mobile access
- **Settings panel** - Full configuration options
- **Context menu** - Right-click integration

---

## 💡 Pro Tips

1. **Pin important files** (⭐) so they don't auto-expire
2. **Use context menu** for fastest sharing from Windows Explorer
3. **Enable autostart** so ShareJadPi is always available
4. **Set file expiry** to auto-clean temporary shares
5. **Bookmark the URL** on your phone for quick access
6. **Use clipboard sync** for quick text transfers
7. **Run speed test** if downloads feel slow

---

## 🔧 Advanced Usage

### Command Line Sharing
```bash
# Share a file from command line
python sharejadpi.py share "C:\path\to\file.txt"

# Share a folder
python sharejadpi.py share "C:\Users\Documents\MyFolder"
```

### Custom Port
Edit `sharejadpi.py` and change the `PORT` variable (default: 5000)

### Custom Token
Set environment variable:
```powershell
$env:SHAREJADPI_TOKEN = "your-custom-token-here"
```

### Disable Auth (Testing Only)
```powershell
$env:SJ_OPEN = "1"
python sharejadpi.py
```
**⚠️ Warning:** Only use this on trusted networks!

---

## 📂 Data Storage Locations

### Windows
- **App data:** `%LOCALAPPDATA%\ShareJadPi\`
  - `shared\` - Files shared from PC (context menu or command line)
  - `uploads\` - Files uploaded from mobile devices
  - `registry.json` - Settings and configuration

### Cleanup
- Files auto-delete based on expiry setting
- Pinned files never auto-delete
- Use "Clear Cache" in settings for manual cleanup
- Locked files are scheduled for deletion on next reboot

---

## 🤝 Workflow Examples

### Example 1: Share Documents to Phone
1. Right-click document → "Share with ShareJadPi"
2. Scan QR code with phone
3. Download on phone
4. File auto-deletes after expiry time

### Example 2: Upload Photos from Phone
1. Open ShareJadPi URL on phone (bookmarked)
2. Drag photos from gallery
3. See upload progress
4. Access photos on PC at `%LOCALAPPDATA%\ShareJadPi\uploads\`

### Example 3: Transfer Text Between Devices
1. Open ShareJadPi on phone
2. Paste text in Shared Clipboard
3. Click Save
4. Text appears on PC automatically (and vice versa)

### Example 4: Share Entire Project Folder
1. Right-click project folder → "Share with ShareJadPi"
2. ShareJadPi zips it in background
3. See progress (speed, ETA, percentage)
4. Download zip on mobile when ready

---

For troubleshooting help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
