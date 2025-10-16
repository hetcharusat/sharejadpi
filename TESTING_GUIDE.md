# Quick Start Testing Guide - Online Sharing Feature

## 🚀 Quick Test (5 Minutes)

### Prerequisites
✅ pyngrok installed (`pip install pyngrok`)  
✅ ShareJadPi server not running yet  
✅ Internet connection available  

---

## Step 1: Install Context Menu

```powershell
# Navigate to ShareJadPi directory
cd C:\Users\hetp2\OneDrive\Desktop\sharejadpi

# Install context menu entries
python sharejadpi.py install-context-menu
```

**Expected Output:**
```
[CTX] install (user) -> OK
```

---

## Step 2: Start ShareJadPi Server

```powershell
python sharejadpi.py
```

**Expected Output:**
```
============================================================
🚀 ShareJadPi - Local File Sharing Server
============================================================

📱 Access from mobile: http://192.168.x.x:5000/?k=...
💻 Access from this PC: http://127.0.0.1:5000/?k=...

🌐 Detected local IPv4s:
   - http://192.168.x.x:5000

✅ Server is running!
...
```

**Keep this terminal open!**

---

## Step 3: Test Online Sharing

### Option A: Via Context Menu (Recommended)

1. Open Windows Explorer
2. Navigate to any test file (e.g., a small PDF or image)
3. Right-click the file
4. Look for two options:
   - ✅ **"Share with ShareJadPi (Local)"**
   - ✅ **"Share with ShareJadPi (Online)"** ← Click this one
5. QR code popup should appear in your browser
6. Check the terminal for output

**Expected Terminal Output:**
```
[NGROK] Starting tunnel to port 5000...
[NGROK] Idle timeout: 15 minutes (file size: 1.2 MB)
[NGROK] ✓ Tunnel active: https://abc1234.ngrok.io
[ONLINE] ✓ Share created: test.pdf
[ONLINE] Token: a1b2c3d4e5f6g7h8...
[ONLINE] URL: https://abc1234.ngrok.io/online-download/a1b2c3d4...
```

**Expected Browser:**
- QR code displayed
- Public URL shown
- Warning about one-time use
- Timeout information

### Option B: Via API (Advanced)

Open a second PowerShell terminal:

```powershell
# Create a test file
echo "Test content" > C:\temp\test.txt

# Share it online
curl -X POST http://127.0.0.1:5000/api/share-online `
  -H "Content-Type: application/json" `
  -d '{\"path\":\"C:\\temp\\test.txt\"}'
```

**Expected Response:**
```json
{
  "success": true,
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "url": "https://abc1234.ngrok.io/online-download/a1b2...",
  "file_name": "test.txt",
  "file_size": "13 B",
  "qr_available": true
}
```

---

## Step 4: Test Download

### From Another Device (Mobile/Tablet)

1. Open the QR code popup from Step 3
2. Scan with your phone camera
3. Tap the link that appears
4. File should download
5. Check terminal - file should be auto-deleted

### From Same PC (Browser)

1. Copy the URL from the QR popup or API response
2. Open in incognito/private browser window
3. File downloads
4. Try accessing the URL again → Should show "Link Already Used"

**Expected Terminal Output:**
```
[ONLINE] Serving file: test.pdf (token: a1b2c3d4e5f6...)
[ONLINE] ✓ Cleaned up: test.pdf
[ONLINE] No more active shares - tunnel will auto-stop on idle timeout
```

---

## Step 5: Verify Cleanup

### Check Active Shares

```powershell
curl http://127.0.0.1:5000/api/online-shares
```

**Expected Response (after download):**
```json
{
  "shares": [],
  "tunnel_active": true,
  "public_url": "https://abc1234.ngrok.io",
  "timeout_minutes": 15
}
```

### Check File System

```powershell
# Check online shares directory
ls "$env:LOCALAPPDATA\ShareJadPi\online_shares"
```

**Expected:** Directory should be empty (files deleted after download)

---

## Step 6: Test Folder Sharing

1. Create a test folder with some files:
   ```powershell
   mkdir C:\temp\test_folder
   echo "File 1" > C:\temp\test_folder\file1.txt
   echo "File 2" > C:\temp\test_folder\file2.txt
   ```

2. Right-click the folder in Explorer
3. Select "Share with ShareJadPi (Online)"
4. Watch terminal for zipping progress

**Expected Terminal Output:**
```
[ONLINE] Zipping folder: C:\temp\test_folder
[NGROK] Starting tunnel to port 5000...
[NGROK] Idle timeout: 15 minutes (file size: 2.5 KB)
[NGROK] ✓ Tunnel active: https://xyz5678.ngrok.io
[ONLINE] ✓ Share created: test_folder_20241016_143022.zip
```

5. Download the ZIP file using the URL
6. Extract and verify contents

---

## Step 7: Test Idle Timeout

1. Create an online share (any file)
2. **Do not download it**
3. Wait 15 minutes (or adjust timeout in code for faster testing)
4. Check terminal

**Expected Terminal Output (after 15 min):**
```
[NGROK] Idle timeout reached (15 min) - shutting down tunnel
[NGROK] Stopping tunnel...
[NGROK] ✓ Tunnel stopped
```

---

## 🧪 Advanced Tests

### Test 1: Large File (Near 2GB Limit)

```powershell
# Create a large test file (500MB)
fsutil file createnew C:\temp\largefile.bin 524288000

# Share it
# Right-click → Share with ShareJadPi (Online)
```

**Expected:** Higher timeout calculated (15 + ~4 min = 19 min)

### Test 2: File Too Large

```powershell
# Create a 3GB file (exceeds limit)
fsutil file createnew C:\temp\toolarge.bin 3221225472

# Try to share it
```

**Expected:** Error message about file size limit

### Test 3: Multiple Shares

1. Share file A
2. Share file B (before downloading A)
3. Check `/api/online-shares` - should show both
4. Download A → should auto-delete only A
5. Download B → should auto-delete B and stop tunnel

---

## ✅ Success Criteria

- [x] Context menu shows both Local and Online options
- [x] QR code popup appears after sharing
- [x] Ngrok tunnel starts successfully
- [x] Public URL is accessible from other devices
- [x] Files download correctly
- [x] Files are deleted after first download
- [x] Second download attempt shows "Link Already Used"
- [x] Folders are automatically zipped
- [x] Idle timeout works (tunnel stops after inactivity)
- [x] File size validation prevents >2GB uploads
- [x] No errors in terminal logs

---

## 🐛 Troubleshooting

### Error: "Ngrok not available"

**Solution:**
```powershell
pip install pyngrok
```

### Error: "ShareJadPi server is not running"

**Solution:** Start the server first:
```powershell
python sharejadpi.py
```

### Context menu not showing

**Solution:** Reinstall context menu:
```powershell
python sharejadpi.py install-context-menu
# Restart Explorer: taskkill /f /im explorer.exe & start explorer.exe
```

### Tunnel won't start

**Possible causes:**
1. No internet connection
2. Ngrok rate limit reached (wait 1 hour)
3. Firewall blocking outbound HTTPS

**Debug:**
```python
python -c "from pyngrok import ngrok; print(ngrok.connect(5000))"
```

### QR popup doesn't open

**Solution:** Manually open:
```
http://127.0.0.1:5000/popup-online?url=YOUR_SHARE_URL
```

---

## 📊 Test Results Template

```
=== ShareJadPi Online Sharing Test Results ===

Date: _______________
Tester: _______________

✅ / ❌  Context menu installation
✅ / ❌  Server startup
✅ / ❌  File sharing via context menu
✅ / ❌  Folder sharing (auto-zip)
✅ / ❌  QR code generation
✅ / ❌  Public URL access from mobile
✅ / ❌  File download success
✅ / ❌  One-time access enforcement
✅ / ❌  Automatic cleanup
✅ / ❌  Idle timeout (15 min)
✅ / ❌  Large file handling
✅ / ❌  Size limit validation (2GB)

Notes:
_________________________________
_________________________________
_________________________________

Overall Status: PASS / FAIL
```

---

## 🎯 Next Steps After Testing

If all tests pass:

1. **Update version** to v3.2.0
2. **Build executable** with PyInstaller
3. **Create installer** with Inno Setup
4. **Update README** with online sharing feature
5. **Create release notes**
6. **Publish GitHub release**

If tests fail:

1. Document specific failures
2. Check console logs for errors
3. Report issues for debugging
4. Iterate on fixes

---

## 📝 Quick Reference

**Start Server:**
```powershell
python sharejadpi.py
```

**Install Context Menu:**
```powershell
python sharejadpi.py install-context-menu
```

**Check Online Shares:**
```powershell
curl http://127.0.0.1:5000/api/online-shares
```

**Manual Cleanup:**
```powershell
curl -X POST http://127.0.0.1:5000/api/online-cleanup
```

**Verify Ngrok:**
```powershell
python -c "from pyngrok import ngrok; print('Ngrok OK')"
```

---

**Happy Testing! 🎉**
