import sys
import os

print("="*60)
print("PyInstaller Bundle Test")
print("="*60)

print(f"\nFrozen: {getattr(sys, 'frozen', False)}")
print(f"sys.executable: {sys.executable}")

if getattr(sys, 'frozen', False):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    print(f"\nsys._MEIPASS: {getattr(sys, '_MEIPASS', 'NOT FOUND')}")
    print(f"Bundle dir: {bundle_dir}")
    
    if os.path.exists(bundle_dir):
        print(f"\nBundle directory contents:")
        items = os.listdir(bundle_dir)
        for item in sorted(items):
            full_path = os.path.join(bundle_dir, item)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path) / (1024*1024)
                print(f"  [FILE] {item} ({size:.2f} MB)")
            else:
                print(f"  [DIR]  {item}/")
        
        cloudflared_path = os.path.join(bundle_dir, 'cloudflared.exe')
        print(f"\nLooking for: {cloudflared_path}")
        print(f"Exists: {os.path.exists(cloudflared_path)}")
    else:
        print(f"\nERROR: Bundle directory does not exist!")
else:
    print("\nNot running as frozen/bundled executable")

print("\n" + "="*60)
input("Press Enter to exit...")
