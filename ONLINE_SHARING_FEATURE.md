# ShareJadPi Online Sharing Feature

## Overview

The Online Sharing feature allows users to temporarily share files or folders publicly over the internet using Ngrok tunnels. This feature provides one-time, secure access to shared content with automatic cleanup and dynamic idle timeouts.

## Features

### ✨ Key Capabilities

1. **Right-Click Integration**
   - "Share with ShareJadPi (Local)" - Local network sharing
   - "Share with ShareJadPi (Online)" - Public internet sharing

2. **Automatic Folder Zipping**
   - Folders are automatically zipped before sharing
   - Progress tracking during compression
   - Maintains original folder structure

3. **Size Limits**
   - Maximum file/folder size: **2 GB**
   - Automatic size validation before processing

4. **Dynamic Idle Timeout**
   - Base timeout: **15 minutes**
   - Additional time: **+2 minutes per 200MB**
   - Example: 1GB file = 15 + (5 × 2) = **25 minutes** idle timeout

5. **One-Time Access**
   - Unique token generated for each share
   - Link expires after first download
   - Automatic file cleanup after use

6. **Ngrok Integration**
   - Ephemeral tunnels (no login required)
   - HTTPS public URLs automatically generated
   - Automatic tunnel shutdown when idle

7. **QR Code Generation**
   - Instant QR code popup after sharing
   - Easy mobile device access
   - Embedded in share notification page

## Technical Implementation

### Components

#### 1. NgrokManager Class
- Manages tunnel lifecycle
- Tracks idle activity with configurable timeouts
- Calculates dynamic timeout based on file size
- Auto-shutdown on inactivity

```python
# Dynamic timeout calculation
Base: 15 minutes
+ (file_size_mb / 200) × 2 minutes
Min: 15 minutes
```

#### 2. OnlineShareManager Class
- Token-based access control
- One-time download enforcement
- Automatic file cleanup after access
- QR code generation for shares

#### 3. Flask Routes

**`/api/share-online` (POST)**
- Handles online share creation
- Validates file size limits
- Zips folders automatically
- Returns token and public URL

**`/online-download/<token>` (GET)**
- Public download endpoint
- Token validation
- One-time access enforcement
- Automatic cleanup after download

**`/api/online-shares` (GET)**
- Lists all active online shares
- Shows tunnel status
- Displays timeout information

**`/api/online-cleanup` (POST)**
- Manual cleanup of all shares
- Stops Ngrok tunnel
- Removes temporary files

**`/popup-online` (GET)**
- QR code display page
- Share URL with copy button
- Timeout information

### File Structure

```
CORE_DIR/
├── shared/                 # Local shares
├── uploads/                # Uploaded files
└── online_shares/          # Online shares (temporary)
    ├── file_20241016_143022.pdf
    └── folder_20241016_143100.zip
```

## Usage

### From Context Menu

1. **Right-click any file or folder**
2. **Select "Share with ShareJadPi (Online)"**
3. **QR code popup appears automatically**
4. **Share the URL or scan QR code**
5. **File auto-deletes after download**

### From UI (Future Enhancement)

A dedicated "Online Shares" tab will display:
- Active online shares
- Public URLs with copy button
- QR codes for each share
- Remaining timeout
- Access status

## Security Considerations

### ✅ Secure Features

- **One-time access tokens** (32-byte random, URL-safe)
- **Automatic expiration** after download or timeout
- **HTTPS by default** (via Ngrok)
- **No persistent public exposure**
- **File cleanup** after use

### ⚠️ Important Notes

1. **Ngrok Free Tier Limits:**
   - 1 tunnel at a time
   - 40 connections per minute
   - Tunnel URL changes each session

2. **File Size Limits:**
   - 2GB max prevents network abuse
   - Large files may timeout during upload

3. **Privacy:**
   - Anyone with the link can download (before first access)
   - Tokens are cryptographically secure but shareable
   - No authentication beyond token possession

## Installation & Setup

### Requirements

```bash
pip install pyngrok
```

### Context Menu Installation

The context menu is automatically installed on first run. To manually reinstall:

```bash
python sharejadpi.py install-context-menu
```

### Verification

1. Start ShareJadPi server
2. Right-click any file
3. Look for two menu options:
   - Share with ShareJadPi (Local)
   - Share with ShareJadPi (Online)

## Configuration

### Environment Variables

```bash
# Custom port (default: 5000)
PORT=8080 python sharejadpi.py
```

### Constants (in code)

```python
MAX_ONLINE_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
BASE_TIMEOUT_MINUTES = 15                       # Base idle timeout
TIMEOUT_INCREMENT_PER_200MB = 2                 # Additional time per 200MB
```

## Monitoring & Troubleshooting

### Check Active Shares

```bash
# Via API
curl http://127.0.0.1:5000/api/online-shares

# Response includes:
# - Active shares list
# - Tunnel status
# - Public URL
# - Timeout minutes
```

### Console Logs

```
[NGROK] Starting tunnel to port 5000...
[NGROK] Idle timeout: 15 minutes (file size: 125.5 MB)
[NGROK] ✓ Tunnel active: https://abc123.ngrok.io
[ONLINE] ✓ Share created: document.pdf
[ONLINE] Token: a1b2c3d4e5f6g7h8...
[ONLINE] URL: https://abc123.ngrok.io/online-download/a1b2c3d4e5f6g7h8...
[ONLINE] Serving file: document.pdf (token: a1b2c3d4e5f6...)
[ONLINE] ✓ Cleaned up: document.pdf
[NGROK] Idle timeout reached (15 min) - shutting down tunnel
```

### Common Issues

**Issue:** "Ngrok not available"
**Solution:** `pip install pyngrok`

**Issue:** Timeout during large folder compression
**Solution:** Share as ZIP manually or split into smaller archives

**Issue:** "Tunnel failed to start"
**Solution:** Check internet connection; Ngrok may be rate-limited

**Issue:** Link expires too quickly
**Solution:** Increase `BASE_TIMEOUT_MINUTES` for longer idle periods

## Performance Characteristics

### Memory Usage

- **Base (idle):** ~50 MB (Flask only)
- **With Ngrok:** ~70-80 MB (adds 20-30 MB)
- **During zip:** +temporary disk I/O (not RAM-resident)

### Network

- **Upload speed:** Limited by Ngrok free tier and local bandwidth
- **Download speed:** Typically 5-50 Mbps on free tier
- **Concurrent downloads:** 1 (one-time access)

### File Operations

- **Copy to online_shares/:** Fast (local disk)
- **Folder compression:** ~10-50 MB/s (depends on CPU)
- **Cleanup:** Instant (simple delete)

## Future Enhancements

### Planned Features

1. **UI Integration**
   - Dedicated "Online Shares" tab in web interface
   - Real-time share status updates
   - Manual share creation from UI

2. **Advanced Options**
   - Custom expiration times
   - Password protection
   - Multiple downloads before expiration

3. **Analytics**
   - Download tracking
   - Bandwidth usage statistics
   - Share history

4. **Notifications**
   - Desktop notification on download
   - Email/SMS alerts (with user config)
   - Webhook support

## API Reference

### Create Online Share

```http
POST /api/share-online
Content-Type: application/json

{
  "path": "C:\\Users\\Documents\\file.pdf"
}

Response:
{
  "success": true,
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "url": "https://abc123.ngrok.io/online-download/a1b2...",
  "file_name": "file.pdf",
  "file_size": "1.2 MB",
  "qr_available": true
}
```

### Download File

```http
GET /online-download/<token>

Response: File download or error HTML page
```

### List Active Shares

```http
GET /api/online-shares

Response:
{
  "shares": [
    {
      "token": "a1b2c3d4e5f6g7h8...",
      "name": "file.pdf",
      "size": "1.2 MB",
      "created_at": "2024-10-16 14:30:22",
      "accessed": false,
      "access_count": 0,
      "url": "https://abc123.ngrok.io/online-download/a1b2..."
    }
  ],
  "tunnel_active": true,
  "public_url": "https://abc123.ngrok.io",
  "timeout_minutes": 15
}
```

### Cleanup All Shares

```http
POST /api/online-cleanup

Response:
{
  "success": true,
  "message": "All online shares cleaned up"
}
```

## License

Same as ShareJadPi main project (see LICENSE file).

## Support

For issues, questions, or feature requests related to online sharing:
1. Check console logs for error messages
2. Verify Ngrok installation: `pip show pyngrok`
3. Test with small files first
4. Check network connectivity

---

**Created:** October 16, 2025  
**Version:** 3.2.0 (Online Sharing Feature)  
**Author:** ShareJadPi Development Team
