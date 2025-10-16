#!/usr/bin/env python3
"""Quick test to see ngrok error"""
import sys
import os

# Test if pyngrok is installed
try:
    from pyngrok import ngrok
    print("✓ pyngrok imported OK")
except ImportError as e:
    print(f"✗ pyngrok import failed: {e}")
    sys.exit(1)

# Try to start a tunnel
try:
    print("\nAttempting to start ngrok tunnel on port 5000...")
    tunnel = ngrok.connect(5000, bind_tls=True)
    print(f"✓ Tunnel started successfully!")
    print(f"  Public URL: {tunnel.public_url}")
    
    # Stop it
    ngrok.disconnect(tunnel.public_url)
    print("✓ Tunnel disconnected")
    
except Exception as e:
    print(f"✗ Ngrok failed: {e}")
    print(f"\nError type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    
    # Check if authtoken is the issue
    if "authtoken" in str(e).lower() or "account" in str(e).lower():
        print("\n" + "="*60)
        print("SOLUTION: Ngrok requires an auth token")
        print("="*60)
        print("1. Go to https://ngrok.com and sign up (free)")
        print("2. Copy your authtoken from the dashboard")
        print("3. Set it in PowerShell:")
        print("   $env:NGROK_AUTHTOKEN = 'YOUR_TOKEN_HERE'")
        print("4. Restart ShareJadPi server")
        print("="*60)
