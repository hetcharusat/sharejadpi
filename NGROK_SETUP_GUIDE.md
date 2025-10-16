# ShareJadPi Online Sharing Setup Guide

## Issue: Ngrok Requires Authentication

As of 2024, Ngrok requires a **free account and authtoken** to create public tunnels.

## Quick Setup (5 minutes)

### Step 1: Create Free Ngrok Account
1. Go to https://dashboard.ngrok.com/signup
2. Sign up with email or GitHub (it's free!)
3. Verify your email if required

### Step 2: Get Your Authtoken
1. After logging in, go to https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy the authtoken (looks like: `2abc...xyz123`)

### Step 3: Configure ShareJadPi

**Option A: Current Session Only (Temporary)**
```powershell
# In PowerShell terminal:
$env:NGROK_AUTHTOKEN = "paste_your_token_here"

# Then restart ShareJadPi server:
Stop-Process -Name python -Force
Start-Process python -ArgumentList "sharejadpi.py" -WindowStyle Normal
```

**Option B: Permanent Setup (Recommended)**
```powershell
# Set permanently for your Windows user:
[System.Environment]::SetEnvironmentVariable('NGROK_AUTHTOKEN', 'paste_your_token_here', 'User')

# Restart your terminal window or log out/in for it to take effect
# Then start ShareJadPi normally
```

### Step 4: Test Online Sharing
1. Make sure ShareJadPi server is running
2. Right-click any file → **Share with ShareJadPi (Online)**
3. Browser opens with "Preparing your public link…"
4. Wait 10-30 seconds → auto-redirects to public URL
5. Share the URL or QR code with anyone!

## How It Works

- **Local sharing** (no Ngrok): Only devices on your WiFi can access
  - URL: `http://192.168.1.11:5000`
  - Fast, no setup needed

- **Online sharing** (with Ngrok): Anyone on internet can access
  - URL: `https://abc123.ngrok.io`
  - Requires free authtoken (one-time setup)
  - Auto-expires after timeout (15min + 2min per 200MB)

## Troubleshooting

**Q: Still getting auth errors after setting token?**
- Make sure you restarted the ShareJadPi server window
- Check token was set: `echo $env:NGROK_AUTHTOKEN` (should show your token)
- Restart your terminal if using Option B

**Q: "Tunnel not found" or "failed to reconnect"?**
- Ngrok free tier allows 1 tunnel at a time
- Close other ngrok processes: `Stop-Process -Name ngrok -Force`
- Try again

**Q: Taking too long?**
- First time: pyngrok downloads ngrok binary (~20MB) - can take 1-2 minutes
- Subsequent runs: 10-30 seconds typically

**Q: Want to stop the tunnel?**
- It stops automatically after the timeout
- Or close the ShareJadPi server window

## Security Notes

- The public URL includes your secret token: `?k=...`
- Only people with the full URL can access your files
- Tunnel auto-expires - not permanent
- Free Ngrok tier: fine for personal use
  - Paid tiers: more features, custom domains, longer tunnels

## Need Help?

- Ngrok docs: https://ngrok.com/docs
- Error codes: https://ngrok.com/docs/errors/
- ShareJadPi: Check the terminal window for detailed logs
