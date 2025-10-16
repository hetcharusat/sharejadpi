import os
import sys
import socket
import secrets
import urllib.parse
import qrcode
import webbrowser
import threading
import time
from flask import Flask, render_template, request, send_file, jsonify, send_from_directory, redirect, make_response, g, abort
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import shutil
import logging
import platform
try:
    import winreg  # type: ignore
except ImportError:
    winreg = None
try:
    import pystray
    from PIL import Image as PILImage, ImageDraw as PILImageDraw
except ImportError:
    pystray = None
import stat
import ctypes
import re
import uuid

# Configuration and app setup (restored)
def resource_path(*paths: str) -> str:
    """Return an absolute path to resource, supporting PyInstaller (_MEIPASS)."""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  # type: ignore[attr-defined]
    return os.path.join(base, *paths)

BASE_DIR = resource_path()

# Core persistent directory (single location for all shared artifacts)
LOCAL_APPDATA = os.getenv('LOCALAPPDATA')
if LOCAL_APPDATA:
    CORE_DIR = os.path.join(LOCAL_APPDATA, 'ShareJadPi')
else:
    CORE_DIR = os.path.join(BASE_DIR, 'core_data')
SHARED_DIR = os.path.join(CORE_DIR, 'shared')
UPLOADS_CORE_DIR = os.path.join(CORE_DIR, 'uploads')
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(UPLOADS_CORE_DIR, exist_ok=True)

# Legacy variable retained
UPLOAD_FOLDER = SHARED_DIR
MAX_FILE_SIZE = 50 * 1024 * 1024 * 1024  # 50GB
MAX_CLIP_SIZE = 1 * 1024 * 1024  # 1MB for text clips
PORT = 5000

app = Flask(__name__, template_folder=resource_path('templates'), static_folder=None)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Static assets directory
STATIC_DIR = resource_path('static')
os.makedirs(STATIC_DIR, exist_ok=True)

# Simple shared clipboard (ephemeral, in-memory)
CLIPBOARD_TEXT = ''
CLIPBOARD_UPDATED = 0.0
SECRET_TOKEN = os.environ.get('SHAREJADPI_TOKEN') or secrets.token_urlsafe(24)
OPEN_MODE = str(os.environ.get('SJ_OPEN', '0')).lower() in ('1','true','yes','on')

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_RUN_NAME = "ShareJadPi"

def get_python_exe():
    return sys.executable

def get_start_command():
    # If frozen (PyInstaller), just run the EXE itself; otherwise run the script with Python
    if getattr(sys, 'frozen', False):  # type: ignore[attr-defined]
        return f'"{sys.executable}"'
    return f'"{get_python_exe()}" "{os.path.abspath(__file__)}"'

# Context menu installation (current user; no admin required)
CM_USER_FILE_KEY = r"Software\Classes\*\shell\ShareJadPi"
CM_USER_DIR_KEY = r"Software\Classes\Directory\shell\ShareJadPi"

def _current_exe_for_context() -> str:
    if getattr(sys, 'frozen', False):  # type: ignore[attr-defined]
        return sys.executable
    return f'{get_python_exe()} "{os.path.abspath(__file__)}"'

def _cm_command_for_exe(exe_path: str) -> str:
    # Quotes around path and argument target
    if 'sharejadpi.py' in exe_path.lower():
        # Running as script
        return f'"{get_python_exe()}" "{os.path.abspath(__file__)}" share "%1"'
    return f'"{exe_path}" share "%1"'

def _reg_set_string(root, path: str, name: str, value: str):
    if not winreg:
        return False
    try:
        with winreg.CreateKey(root, path) as k:  # type: ignore[union-attr]
            winreg.SetValueEx(k, name, 0, winreg.REG_SZ, value)  # type: ignore[union-attr]
        return True
    except Exception:
        return False

def _reg_key_exists(root, path: str) -> bool:
    if not winreg:
        return False
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ):  # type: ignore[union-attr]
            return True
    except Exception:
        return False

def _reg_get_string(root, path: str, name: str) -> str:
    if not winreg:
        return ""
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as k:  # type: ignore[union-attr]
            v, _ = winreg.QueryValueEx(k, name)  # type: ignore[union-attr]
            return str(v)
    except Exception:
        return ""

def _reg_delete_tree(root, path: str):
    if not winreg:
        return False
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:  # type: ignore[union-attr]
            # enumerate subkeys and delete recursively
            i = 0
            try:
                while True:
                    sub = winreg.EnumKey(key, i)  # type: ignore[union-attr]
                    _reg_delete_tree(root, path + "\\" + sub)
                    i += 1
            except OSError:
                pass
        winreg.DeleteKey(root, path)  # type: ignore[union-attr]
        return True
    except Exception:
        return False

def context_menu_installed_user() -> bool:
    if not winreg:
        return False
    exe = _current_exe_for_context()
    expected = _cm_command_for_exe(exe)
    cmd1 = _reg_get_string(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY + "\\command", "")
    cmd2 = _reg_get_string(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY + "\\command", "")
    return (expected.lower() == cmd1.lower()) and (expected.lower() == cmd2.lower())

def install_context_menu_user() -> bool:
    if platform.system() != 'Windows' or not winreg:
        return False
    exe = _current_exe_for_context()
    cmd = _cm_command_for_exe(exe)
    ok = True
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY, "", "Share with ShareJadPi")
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY, "Icon", exe)
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY + "\\command", "", cmd)
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY, "", "Share with ShareJadPi")
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY, "Icon", exe)
    ok &= _reg_set_string(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY + "\\command", "", cmd)
    return ok

 

def uninstall_context_menu_user() -> bool:
    if platform.system() != 'Windows' or not winreg:
        return False
    ok1 = _reg_delete_tree(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY + "\\command")
    ok1 &= _reg_delete_tree(winreg.HKEY_CURRENT_USER, CM_USER_FILE_KEY)
    ok2 = _reg_delete_tree(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY + "\\command")
    ok2 &= _reg_delete_tree(winreg.HKEY_CURRENT_USER, CM_USER_DIR_KEY)
    return ok1 and ok2

def is_autostart_enabled():
    if platform.system() != 'Windows' or not winreg:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, APP_RUN_NAME)
            expected = get_start_command()
            return val == expected
    except FileNotFoundError:
        return False
    except Exception:
        return False

def enable_autostart():
    if platform.system() != 'Windows' or not winreg:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_RUN_NAME, 0, winreg.REG_SZ, get_start_command())
        return True
    except FileNotFoundError:
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH) as key:
                winreg.SetValueEx(key, APP_RUN_NAME, 0, winreg.REG_SZ, get_start_command())
            return True
        except Exception:
            return False
    except Exception:
        return False

def disable_autostart():
    if platform.system() != 'Windows' or not winreg:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_RUN_NAME)
        return True
    except FileNotFoundError:
        return True
    except Exception:
        return False

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def _get_all_local_ips():
    """Return a set of local IPs (IPv4/IPv6) for the host machine, incl. loopbacks."""
    ips = set(["127.0.0.1", "::1"])
    try:
        hostname = socket.gethostname()
        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                infos = socket.getaddrinfo(hostname, None, family, socket.SOCK_STREAM)
                for info in infos:
                    ip = info[4][0]
                    if ip:
                        ips.add(str(ip))
            except Exception:
                pass
    except Exception:
        pass
    # Primary outbound IPv4 via UDP connect trick
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return list(ips)

def get_access_url(with_token: bool = True) -> str:
    """Return an http URL using the active outbound IP (Ethernet/Wi‑Fi), with optional token."""
    host_ip = get_local_ip() or '127.0.0.1'
    base = f"http://{host_ip}:{PORT}/"
    if with_token:
        return base + f"?k={SECRET_TOKEN}"
    return base

def generate_qr_code(url):
    """Generate QR code"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = os.path.join(STATIC_DIR, "qr_code.png")
        
        # Ensure directory exists
        os.makedirs(STATIC_DIR, exist_ok=True)
        
        # Remove existing file if locked
        if os.path.exists(qr_path):
            try:
                os.chmod(qr_path, stat.S_IWRITE)
                os.remove(qr_path)
            except Exception:
                pass
        
        qr_img.save(qr_path)  # type: ignore[arg-type]
        return qr_path
    except Exception as e:
        print(f"[QR] Warning: Could not generate QR code: {e}")
        # Return a placeholder path so app doesn't crash
        return os.path.join(STATIC_DIR, "qr_code.png")

def show_qr_popup(url):
    """Open the dynamic /popup route in default browser."""
    try:
        # ensure QR updated
        generate_qr_code(url)
        webbrowser.open(f'http://127.0.0.1:{PORT}/popup?ts={int(time.time())}')
    except Exception as e:
        print(f"[ERROR] Unable to open QR popup: {e}")

tray_icon = None

# In-memory registry (session-based)
from uuid import uuid4
from threading import Lock
REGISTRY_LOCK = Lock()
ENTRIES = {}  # id -> entry dict
EXPIRY_MINUTES = 10  # default 10 minutes; can be changed in Settings (0 = disabled)

# Live zip job tracking
ZIP_JOBS = {}
ZIP_JOBS_LOCK = Lock()

# Dedicated uploads dir (single-use)
UPLOADS_DIR = UPLOADS_CORE_DIR

def register_entry(path, kind):
    """Register a file path. kind in {'copy','upload','zip'}"""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    st = os.stat(path)
    entry_id = uuid4().hex
    entry = {
        'id': entry_id,
        'name': os.path.basename(path),
        'path': path,
        'size': st.st_size,
        'mtime': st.st_mtime,
        'kind': kind,
        'pinned': False,
        'downloads': 0,
        'added_at': time.time()
    }
    with REGISTRY_LOCK:
        ENTRIES[entry_id] = entry
    return entry

def list_entries():
    with REGISTRY_LOCK:
        return sorted(ENTRIES.values(), key=lambda e: e['added_at'], reverse=True)

def get_entry(entry_id):
    with REGISTRY_LOCK:
        return ENTRIES.get(entry_id)

def remove_entry(entry_id):
    with REGISTRY_LOCK:
        return ENTRIES.pop(entry_id, None)

def mark_download(entry_id):
    with REGISTRY_LOCK:
        e = ENTRIES.get(entry_id)
        if e:
            e['downloads'] += 1
        return e

def purge_expired():
    if EXPIRY_MINUTES <= 0:
        return 0
    threshold = time.time() - (EXPIRY_MINUTES * 60)
    removed = 0
    for e in list_entries():
        if e.get('pinned'):
            continue
        if e['added_at'] < threshold:
            ent = remove_entry(e['id'])
            if ent and ent['kind'] in ('upload','zip','copy'):
                try:
                    if os.path.exists(ent['path']):
                        _force_delete(ent['path'])
                except Exception:
                    pass
            removed += 1
    return removed

def cleanup_loop():
    while True:
        try:
            purge_expired()
        except Exception:
            pass
        time.sleep(60)  # run every minute

def create_tray_image():
    # Simple green circle icon
    img = PILImage.new('RGB', (64,64), color=(76,175,80))
    d = PILImageDraw.Draw(img)
    d.ellipse((8,8,56,56), outline=(255,255,255), width=4)
    d.text((22,22), 'S', fill=(255,255,255))
    return img

def tray_open_share(icon, item):  # noqa: ARG001
    try:
        webbrowser.open(get_access_url(with_token=True))
    except Exception:
        pass

def tray_show_qr(icon, item):  # noqa: ARG001
    url = get_access_url(with_token=True)
    show_qr_popup(url)

def tray_open_settings(icon, item):  # noqa: ARG001
    webbrowser.open(get_access_url(with_token=True) + 'settings')

def tray_quit(icon, item):  # noqa: ARG001
    global tray_icon
    if icon:
        icon.stop()
    print("\n[QUIT] Exiting ShareJadPi...")
    os._exit(0)

def start_tray():
    global tray_icon
    if not pystray:
        print("[TRAY] pystray not installed; tray icon disabled")
        return
    image = create_tray_image()
    def tray_install_cm(icon, item):  # noqa: ARG001
        ok = install_context_menu_user()
        print(f"[CTX] Install (user) -> {'OK' if ok else 'FAILED'}")
    def tray_uninstall_cm(icon, item):  # noqa: ARG001
        ok = uninstall_context_menu_user()
        print(f"[CTX] Uninstall (user) -> {'OK' if ok else 'FAILED'}")
    def tray_clear_cache(icon, item):  # noqa: ARG001
        cleared_ids = []
        for e in list_entries():
            cleared_ids.append(e['id'])
        file_deletes = 0
        errs = []
        for rid in cleared_ids:
            ent = remove_entry(rid)
            if ent and ent['kind'] in ('upload','zip','copy'):
                ok, err = _force_delete(ent['path'])
                if ok:
                    file_deletes += 1
                elif err:
                    errs.append(f"entry {ent['path']}: {err}")
        extra_deletes = 0
        for base in (SHARED_DIR, UPLOADS_CORE_DIR):
            for root, _, files in os.walk(base):
                for f in files:
                    fp = os.path.join(root, f)
                    ok, err = _force_delete(fp)
                    if ok:
                        extra_deletes += 1
                    elif err:
                        errs.append(f"sweep {fp}: {err}")
        ensure_core_dirs()
        s = _cache_status_dict()
        print(f"[CACHE] Cleared {len(cleared_ids)} entries, deleted_files={file_deletes}, swept_extra={extra_deletes}. Remaining: entries={s['entries_count']}, shared_files={s['uploads_count']}")
        if errs:
            print('[CACHE] Some items scheduled for deletion on reboot or failed:', errs)
    menu = pystray.Menu(
        pystray.MenuItem('Open Share Page', tray_open_share),
        pystray.MenuItem('Show QR', tray_show_qr),
        pystray.MenuItem('Install Context Menu', tray_install_cm),
        pystray.MenuItem('Remove Context Menu', tray_uninstall_cm),
        pystray.MenuItem('Clear Cache', tray_clear_cache),
        pystray.MenuItem('Settings', tray_open_settings),
        pystray.MenuItem('Quit', tray_quit)
    )
    tray_icon = pystray.Icon('ShareJadPi', image, 'ShareJadPi', menu)
    tray_icon.run()

def share_file_or_folder(path):
    """Share by copying file(s) / zipping directories into central shared dir.
    Returns list of created entry dicts."""
    created = []
    try:
        print(f"\n{'='*60}\n[SHARE] Processing: {path}\n{'='*60}")
        if os.path.isfile(path):
            src_name = os.path.basename(path)
            base, ext = os.path.splitext(src_name)
            candidate = src_name
            dest = os.path.join(SHARED_DIR, candidate)
            idx = 1
            while os.path.exists(dest):
                candidate = f"{base}_{idx}{ext}"
                dest = os.path.join(SHARED_DIR, candidate)
                idx += 1
            shutil.copy2(path, dest)
            entry = register_entry(dest, 'copy')
            created.append(entry)
            print(f"[SHARE] ✓ Copied: {entry['name']} -> {entry['id']}")
        elif os.path.isdir(path):
            base_name = os.path.basename(os.path.normpath(path))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            zip_name = f"{base_name}_{timestamp}.zip"
            zip_path = os.path.join(SHARED_DIR, zip_name)
            import zipfile
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(path):
                    for f in files:
                        full = os.path.join(root, f)
                        rel = os.path.relpath(full, path)
                        zf.write(full, arcname=rel)
            entry = register_entry(zip_path, 'zip')
            created.append(entry)
            print(f"[SHARE] ✓ Folder zipped: {entry['name']} -> {entry['id']}")
        else:
            print("[SHARE] Path not found or inaccessible")
        if created:
            url = get_access_url(with_token=True)
            print(f"\n[SUCCESS] {len(created)} item(s) shared! URL: {url}")
            show_qr_popup(url)
        else:
            print("[SHARE] No entries created.")
    except Exception as e:
        print(f"[ERROR] Failed to share: {e}")
        import traceback; traceback.print_exc()
    return created

def format_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

# Utilities for cache stats
def _dir_stats(path):
    files = 0
    bytes_ = 0
    if os.path.isdir(path):
        for root, _, fnames in os.walk(path):
            for f in fnames:
                fp = os.path.join(root, f)
                try:
                    st = os.stat(fp)
                    files += 1
                    bytes_ += st.st_size
                except Exception:
                    pass
    return files, bytes_

def _cache_status_dict():
    shared_c, shared_b = _dir_stats(SHARED_DIR)
    uploads_c, uploads_b = _dir_stats(UPLOADS_CORE_DIR)
    with REGISTRY_LOCK:
        entries_c = len(ENTRIES)
    return {
        'entries_count': entries_c,
        'shared_count': shared_c,
        'shared_bytes': shared_b,
        'uploads_count': uploads_c,
        'uploads_bytes': uploads_b,
    }

# Ensure core dirs helper

def ensure_core_dirs():
    try:
        os.makedirs(CORE_DIR, exist_ok=True)
        os.makedirs(SHARED_DIR, exist_ok=True)
        os.makedirs(UPLOADS_CORE_DIR, exist_ok=True)
    except Exception:
        pass

# Robust delete helper (Windows-friendly)
MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004
try:
    MoveFileExW = ctypes.windll.kernel32.MoveFileExW  # type: ignore[attr-defined]
except Exception:
    MoveFileExW = None

def _force_delete(fp):
    """Try to delete a file with retry logic for locked files."""
    try:
        if not os.path.exists(fp):
            return True, None
        
        # Retry logic for locked files
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Try to make file writable
                try:
                    os.chmod(fp, stat.S_IWRITE)
                except Exception:
                    pass
                
                # Attempt deletion
                os.remove(fp)
                if attempt > 0:
                    print(f"[CLEANUP] Deleted {fp} on attempt {attempt + 1}")
                return True, None
            except PermissionError as e:
                if attempt < max_retries - 1:
                    # Wait a bit and retry
                    time.sleep(0.5)
                    continue
                else:
                    # Last attempt failed
                    err_msg = f"[WinError 32] File locked: {e}"
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                else:
                    err_msg = str(e)
        
        # All retries failed, try schedule delete on reboot (Windows)
        try:
            if MoveFileExW is not None:
                res = MoveFileExW(ctypes.c_wchar_p(fp), None, MOVEFILE_DELAY_UNTIL_REBOOT)
                if res:
                    print(f"[CLEANUP] Scheduled for reboot deletion: {fp}")
                    return False, f"Scheduled for delete on reboot"
        except Exception as e2:
            return False, f"{err_msg}; schedule failed: {e2}"
        
        return False, err_msg
    except Exception as e:
        return False, str(e)

def _zip_job_worker(job_id: str, job_dir: str, zip_path: str):
    """Background worker to zip a staged folder into SHARED_DIR with live progress."""
    start = time.time()
    try:
        import zipfile
        compression = zipfile.ZIP_STORED  # fastest, no compression
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        processed = 0
        files_done = 0

        # Pre-compute total bytes if missing
        with ZIP_JOBS_LOCK:
            job = ZIP_JOBS.get(job_id, {})
            total = job.get('total_bytes') or 0

        # Build list of files to include with relative paths
        file_list = []
        for root, _, files in os.walk(job_dir):
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, job_dir).replace('\\','/')
                file_list.append((full, rel))

        with zipfile.ZipFile(zip_path, 'w', compression=compression, allowZip64=True) as zf:
            for full, rel in file_list:
                try:
                    with open(full, 'rb') as src, zf.open(rel, 'w') as dst:
                        # Larger chunks for throughput (1MB)
                        buf = memoryview(bytearray(1024 * 1024))
                        while True:
                            n = src.readinto(buf)
                            if not n:
                                break
                            dst.write(buf[:n])
                            processed += n
                            # Periodically update job speed/eta
                            if processed % (8 * 1024 * 1024) == 0:  # every 8MB
                                elapsed = max(0.001, time.time() - start)
                                speed = processed / elapsed
                                eta = None
                                if total and speed:
                                    eta = max(0.0, (total - processed) / speed)
                                with ZIP_JOBS_LOCK:
                                    j = ZIP_JOBS.get(job_id)
                                    if j:
                                        j.update({'processed_bytes': processed, 'speed_bps': speed, 'eta_sec': eta, 'files_done': files_done})
                    files_done += 1
                    # Update after each file
                    elapsed = max(0.001, time.time() - start)
                    speed = processed / elapsed
                    eta = None
                    if total and speed:
                        eta = max(0.0, (total - processed) / speed)
                    with ZIP_JOBS_LOCK:
                        j = ZIP_JOBS.get(job_id)
                        if j:
                            j.update({'processed_bytes': processed, 'speed_bps': speed, 'eta_sec': eta, 'files_done': files_done})
                except Exception as ex:
                    print(f"[ZIP] Failed {rel}: {ex}")
                    continue

        # Register entry
        entry = register_entry(zip_path, 'zip')
        with ZIP_JOBS_LOCK:
            j = ZIP_JOBS.get(job_id)
            if j:
                j.update({'status': 'done', 'entry_id': entry['id']})
        print(f"[ZIP] ✓ Job {job_id} complete -> {entry['name']} in {time.time()-start:.1f}s")
    except Exception as e:
        print(f"[ZIP] Job {job_id} error: {e}")
        with ZIP_JOBS_LOCK:
            j = ZIP_JOBS.get(job_id)
            if j:
                j.update({'status': 'error', 'error': str(e)})
        # Cleanup partial zip
        try:
            if os.path.exists(zip_path):
                _force_delete(zip_path)
        except Exception:
            pass
    finally:
        # Remove staging directory
        try:
            if os.path.exists(job_dir):
                shutil.rmtree(job_dir, ignore_errors=True)
        except Exception:
            pass

@app.route('/api/zip_jobs/<job_id>', methods=['GET'])
def api_zip_job(job_id):
    with ZIP_JOBS_LOCK:
        job = ZIP_JOBS.get(job_id)
        if not job:
            return jsonify({'error': 'not-found'}), 404
        # derive percent
        total = job.get('total_bytes') or 0
        done = job.get('processed_bytes') or 0
        pct = (done / total * 100.0) if total > 0 else 0.0
        out = dict(job)
        out['percent'] = pct
        # Reduce float noise
        if out.get('speed_bps'):
            out['speed_bps'] = float(out['speed_bps'])
        if out.get('eta_sec') is not None:
            out['eta_sec'] = float(out['eta_sec'])
        return jsonify(out)

def _is_authorized() -> bool:
    """Check if the current request is authorized (host or valid token/cookie)."""
    # Host PC always authorized
    if is_request_from_host():
        return True
    # Check cookie
    c = request.cookies.get('sjk')
    if c and secrets.compare_digest(c, SECRET_TOKEN):
        return True
    # Check query token
    qtok = request.args.get('k')
    if qtok and secrets.compare_digest(qtok, SECRET_TOKEN):
        return True
    return False

@app.before_request
def _token_gate():
    """Token gate: always allow HTML to render, but block unauthorized API/action requests."""
    # Open mode: disable token gate entirely (for debug/troubleshooting)
    if OPEN_MODE:
        return
    
    # Handle token in URL: set cookie and redirect to clean URL
    qtok = request.args.get('k')
    if qtok and secrets.compare_digest(qtok, SECRET_TOKEN):
        try:
            # Strip k from current URL
            pu = urllib.parse.urlparse(request.full_path if request.query_string else request.path)
            qs = urllib.parse.parse_qs(pu.query)
            qs.pop('k', None)
            pairs = []
            for k, vals in qs.items():
                if isinstance(vals, list):
                    for vv in vals:
                        pairs.append((k, vv))
                else:
                    pairs.append((k, vals))
            new_query = urllib.parse.urlencode(pairs)
            clean_url = pu.path + (('?' + new_query) if new_query else '')
        except Exception:
            clean_url = request.path
        resp = make_response(redirect(clean_url or '/'))
        resp.set_cookie('sjk', SECRET_TOKEN, max_age=7*24*3600, httponly=True, samesite='Lax', path='/')
        return resp
    
    # Public endpoints that don't require authorization (so UI can load and check status)
    public_paths = ['/', '/qr', '/popup', '/health', '/favicon.ico', '/api/status', '/api/is_host']
    if request.path.startswith('/static'):
        public_paths.append(request.path)
    
    # Allow download endpoints (they handle auth internally and need to return files, not JSON)
    if request.path.startswith('/download/'):
        return  # Let download endpoint handle authorization
    
    if request.path in public_paths:
        return  # Allow these to proceed
    
    # All other endpoints require authorization
    if not _is_authorized():
        return jsonify({'error': 'Unauthorized', 'message': 'Valid token required'}), 401

@app.after_request
def _security_headers(resp):
    # Security headers
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resp.headers.setdefault('X-Frame-Options', 'DENY')
    resp.headers.setdefault('Referrer-Policy', 'same-origin')
    resp.headers.setdefault('Permissions-Policy', "geolocation=(), microphone=(), camera=(), display-capture=(), usb=()")
    resp.headers.setdefault('Content-Security-Policy',
        "default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none'")
    
    # Aggressive cache-busting for HTML to prevent stale cached pages
    # This fixes the issue where phones with cached versions take 40-50 seconds to load
    if request.path == '/' or request.path.endswith('.html'):
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
    
    # If we flagged to set the token cookie, attach it now
    try:
        if getattr(g, 'set_token_cookie', False):
            resp.set_cookie('sjk', SECRET_TOKEN, max_age=7*24*3600, httponly=True, samesite='Lax', path='/')
    except Exception:
        pass
    return resp

# Flask routes
@app.route('/')
def index():
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                size_str = format_file_size(size)
                modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                files.append({'name': filename, 'size': size_str, 'modified': modified})
    files.sort(key=lambda x: x['modified'], reverse=True)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if not file or not file.filename:
            return jsonify({'error': 'No selected file'}), 400
        
        filename = secure_filename(file.filename)
        # Ensure unique name in uploads
        base, ext = os.path.splitext(filename)
        candidate = filename
        idx = 1
        filepath = os.path.join(UPLOADS_DIR, candidate)
        while os.path.exists(filepath):
            candidate = f"{base}_{idx}{ext}"
            filepath = os.path.join(UPLOADS_DIR, candidate)
            idx += 1
        
        # Save file with error handling for large files
        try:
            file.save(filepath)
        except Exception as save_err:
            print(f"[ERROR] Failed to save file {filename}: {save_err}")
            return jsonify({'error': f'Failed to save file: {str(save_err)}'}), 500
            
        entry = register_entry(filepath, 'upload')
        print(f"[UPLOAD] ✓ Registered upload: {entry['name']} -> {entry['id']}")
        return jsonify({'success': True, 'id': entry['id'], 'name': entry['name']}), 200
        
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# (Old upload_folder implementation removed; superseded by background job version below)

@app.route('/download/<entry_id>', methods=['GET', 'HEAD'])
def download_entry(entry_id):
    # Downloads are public - if you know the ID, you can download
    # (The file list itself is protected, so unauthorized users won't know IDs)
    e = get_entry(entry_id)
    if not e:
        return jsonify({'error': 'Not found'}), 404
    if not os.path.exists(e['path']):
        remove_entry(entry_id)
        return jsonify({'error': 'File missing'}), 404
    # Important: some mobile browsers issue a HEAD request before GET to probe size.
    # Do not mark/download or delete on HEAD, only return headers.
    if request.method == 'HEAD':
        # Don't use context manager - send_file will close it after streaming
        return send_file(e['path'], as_attachment=True, download_name=e['name'])
    # Real download (GET)
    mark_download(entry_id)
    
    # Send file directly - Flask will handle opening and closing
    response = send_file(
        e['path'],
        as_attachment=True,
        download_name=e['name'],
        mimetype='application/octet-stream'
    )
    
    # Delete upload files after download (but not on Range requests)
    if e['kind'] == 'upload':
        # Only delete when it's a user-initiated download (dl=1) and not a Range probe.
        if request.args.get('dl') == '1' and 'Range' not in request.headers:
            removed = remove_entry(entry_id)
            if removed:
                # Use force delete with retry
                ok, err = _force_delete(removed['path'])
                if not ok:
                    print(f"[CLEANUP] Could not delete {removed['path']}: {err}")
    
    return response

@app.route('/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    e = remove_entry(entry_id)
    if not e:
        return jsonify({'error': 'Not found'}), 404
    if e['kind'] in ('upload','zip','copy'):
        try:
            if os.path.exists(e['path']):
                ok, err = _force_delete(e['path'])
                if not ok and err:
                    print(f"[DELETE] Could not delete {e['path']}: {err}")
        except Exception as de:
            print(f"[DELETE] Error deleting {e['path']}: {de}")
    return jsonify({'success': True}), 200

@app.route('/api/clear', methods=['POST'])
def clear_all():
    ensure_core_dirs()
    before = _cache_status_dict()
    removed_ids = []
    for e in list_entries():
        removed_ids.append(e['id'])
    file_deletes = 0
    errs = []
    for rid in removed_ids:
        ent = remove_entry(rid)
        if ent and ent['kind'] in ('upload','zip','copy'):
            ok, err = _force_delete(ent['path'])
            if ok:
                file_deletes += 1
            elif err:
                errs.append(f"entry {ent['path']}: {err}")
    # Sweep core dirs for any remaining files (safety)
    extra_deletes = 0
    for base in (SHARED_DIR, UPLOADS_CORE_DIR):
        for root, _, files in os.walk(base):
            for f in files:
                fp = os.path.join(root, f)
                ok, err = _force_delete(fp)
                if ok:
                    extra_deletes += 1
                elif err:
                    errs.append(f"sweep {fp}: {err}")
    ensure_core_dirs()
    after = _cache_status_dict()
    print(f"[CACHE] HTTP clear_all: removed_entries={len(removed_ids)}, deleted_files={file_deletes}, swept_extra={extra_deletes} -> remaining: entries={after['entries_count']}, shared_files={after['shared_count']}, uploads_files={after['uploads_count']}")
    return jsonify({'success': True, 'cleared_entries': len(removed_ids), 'deleted_files': file_deletes, 'swept_extra_files': extra_deletes, 'before': before, 'after': after, 'errors': errs})

@app.route('/qr')
def qr_code():
    return send_from_directory(STATIC_DIR, 'qr_code.png')

@app.route('/health')
def health():
    return jsonify({'ok': True, 'ip': get_local_ip(), 'port': PORT})

@app.route('/popup')
def popup():
    """Serve dynamic QR popup page."""
    url = get_access_url(with_token=True)
    # QR will be served from /qr with cache buster in img tag
    return f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>ShareJadPi QR</title>
<style>
body{{margin:0;font-family:Arial,Helvetica,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;background:linear-gradient(135deg,#667eea,#764ba2);color:#222;}}
.card{{background:#fff;padding:32px 42px;border-radius:14px;box-shadow:0 10px 40px rgba(0,0,0,.25);text-align:center;max-width:460px;}}
img{{max-width:320px;width:100%;display:block;margin:0 auto 12px;}}
h1{{font-size:22px;margin:0 0 10px;}}
.url{{font-size:15px;word-break:break-all;color:#4CAF50;margin:4px 0 14px;font-weight:600;}}
.count{{margin-top:10px;font-size:13px;color:#666;}}
button{{margin-top:14px;padding:8px 16px;background:#4CAF50;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:14px;}}
button:hover{{background:#45a049;}}
</style>
<script>
let secs=15;function tick(){{document.getElementById('count').textContent=secs;secs--;if(secs<0){{window.close();}}}}setInterval(tick,1000);
function refreshQR(){{document.getElementById('qr').src='/qr?t='+Date.now();}}
window.onload=()=>{{refreshQR();}};
</script></head>
<body><div class='card'>
<h1>Files Shared!</h1>
<div class='url'>{url}</div>
<img id='qr' alt='QR Code'>
<div class='count'>Auto close in <span id='count'>15</span>s</div>
<button onclick='refreshQR()'>Refresh QR</button>
</div></body></html>"""

@app.route('/api/files')
def api_files():
    rows = []
    to_remove = []
    for e in list_entries():
        if not os.path.exists(e['path']):
            to_remove.append(e['id'])
            continue
        # compute minutes until expiry (rounded up), 0 if disabled
        if EXPIRY_MINUTES > 0:
            elapsed = max(0, int((time.time() - e['added_at']) // 60))
            rem = max(0, EXPIRY_MINUTES - elapsed)
        else:
            rem = 0
        rows.append({
            'id': e['id'],
            'name': e['name'],
            'size': format_file_size(e['size']),
            'kind': e['kind'],
            'added': datetime.fromtimestamp(e['added_at']).strftime('%Y-%m-%d %H:%M:%S'),
            'pinned': bool(e.get('pinned', False)),
            'expires_in': rem,
            'is_new': (time.time() - e['added_at']) < 120
        })
    for rid in to_remove:
        remove_entry(rid)
    return jsonify({'files': rows})

@app.route('/delete_bulk', methods=['POST'])
def delete_bulk():
    try:
        data = request.get_json(silent=True) or {}
        ids = data.get('ids') or []
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            return jsonify({'error': 'ids must be a list of strings'}), 400
        deleted = 0
        errs = []
        for rid in ids:
            ent = remove_entry(rid)
            if ent and ent['kind'] in ('upload','zip','copy'):
                ok, err = _force_delete(ent['path'])
                if ok:
                    deleted += 1
                elif err:
                    errs.append(f"{ent['path']}: {err}")
        return jsonify({'success': True, 'deleted': deleted, 'errors': errs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/zip_selected', methods=['POST'])
def zip_selected():
    try:
        data = request.get_json(silent=True) or {}
        ids = data.get('ids') or []
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            return jsonify({'error': 'ids must be a list of strings'}), 400
        items = []
        for rid in ids:
            e = get_entry(rid)
            if e and os.path.exists(e['path']):
                items.append(e)
        if not items:
            return jsonify({'error': 'no valid items'}), 400
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f"selected_{ts}.zip"
        zip_path = os.path.join(SHARED_DIR, zip_name)
        import zipfile
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for e in items:
                zf.write(e['path'], arcname=e['name'])
        entry = register_entry(zip_path, 'zip')
        return jsonify({'success': True, 'id': entry['id'], 'name': entry['name']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pin', methods=['POST'])
def api_pin():
    try:
        data = request.get_json(silent=True) or {}
        ids = data.get('ids') or []
        pinned = bool(data.get('pinned', True))
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            return jsonify({'error': 'ids must be a list of strings'}), 400
        count = 0
        with REGISTRY_LOCK:
            for rid in ids:
                e = ENTRIES.get(rid)
                if e:
                    e['pinned'] = pinned
                    count += 1
        return jsonify({'success': True, 'updated': count, 'pinned': pinned})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    # Return host and authorization status for Connected badge
    is_host = is_request_from_host()
    authorized = is_host
    if not is_host:
        c = request.cookies.get('sjk')
        authorized = bool(c and secrets.compare_digest(c, SECRET_TOKEN))
    return jsonify({'host': is_host, 'authorized': authorized})

@app.route('/api/autostart', methods=['GET', 'POST'])
def api_autostart():
    if request.method == 'GET':
        return jsonify({'enabled': is_autostart_enabled()})
    data = request.get_json(silent=True) or {}
    # Only host PC can change autostart
    if not is_request_from_host():
        return jsonify({'error': 'Forbidden'}), 403
    enable = data.get('enable')
    if enable is True:
        ok = enable_autostart()
        return jsonify({'enabled': is_autostart_enabled(), 'success': ok})
    elif enable is False:
        ok = disable_autostart()
        return jsonify({'enabled': is_autostart_enabled(), 'success': ok})
    return jsonify({'error': 'Missing enable true/false'}), 400

@app.route('/api/expiry', methods=['GET', 'POST'])
def api_expiry():
    """Get or set automatic expiry (in minutes)."""
    global EXPIRY_MINUTES
    if request.method == 'GET':
        return jsonify({'minutes': EXPIRY_MINUTES, 'enabled': EXPIRY_MINUTES > 0})
    data = request.get_json(silent=True) or {}
    # Only host PC can modify expiry
    if not is_request_from_host():
        return jsonify({'error': 'Forbidden'}), 403
    minutes = data.get('minutes')
    try:
        if minutes is None or minutes == '' or int(minutes) <= 0:
            EXPIRY_MINUTES = 0
            purged = purge_expired()
            return jsonify({'minutes': 0, 'enabled': False, 'purged': purged, 'success': True})
        new_minutes = int(minutes)
    except (ValueError, TypeError):
        return jsonify({'error': 'minutes must be an integer'}), 400
    if new_minutes > 10080:  # clamp to 7 days
        new_minutes = 10080
    EXPIRY_MINUTES = new_minutes
    purged = purge_expired()
    return jsonify({'minutes': EXPIRY_MINUTES, 'enabled': True, 'purged': purged, 'success': True})

@app.route('/api/paths', methods=['GET'])
def api_paths():
    # Only expose local paths to the host PC
    if not is_request_from_host():
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'core': CORE_DIR, 'shared': SHARED_DIR, 'uploads': UPLOADS_CORE_DIR})

@app.route('/api/clipboard', methods=['GET', 'POST', 'DELETE'])
def api_clipboard():
    global CLIPBOARD_TEXT, CLIPBOARD_UPDATED
    if request.method == 'GET':
        return jsonify({'text': CLIPBOARD_TEXT, 'updated': CLIPBOARD_UPDATED})
    if request.method == 'DELETE':
        CLIPBOARD_TEXT = ''
        CLIPBOARD_UPDATED = time.time()
        return jsonify({'success': True, 'text': ''})
    # POST
    data = request.get_json(silent=True)
    text = ''
    if data and isinstance(data, dict) and 'text' in data:
        text = str(data.get('text') or '')
    else:
        if request.mimetype and 'text/plain' in request.mimetype:
            text = request.get_data(as_text=True) or ''
    if len(text.encode('utf-8')) > MAX_CLIP_SIZE:
        return jsonify({'error': 'Text too large (max 1MB)'}), 413
    CLIPBOARD_TEXT = text
    CLIPBOARD_UPDATED = time.time()
    return jsonify({'success': True, 'text': CLIPBOARD_TEXT, 'updated': CLIPBOARD_UPDATED})

@app.route('/api/clip', methods=['POST'])
def api_clip():
    """Accept a text payload and store it as a .txt file for sharing."""
    try:
        # Try JSON first
        data = request.get_json(silent=True)
        text = None
        if data and isinstance(data, dict) and 'text' in data:
            text = str(data.get('text') or '')
        # If not JSON, accept raw text/plain
        if text is None:
            if request.mimetype and 'text/plain' in request.mimetype:
                text = request.get_data(as_text=True)
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        if len(text.encode('utf-8')) > MAX_CLIP_SIZE:
            return jsonify({'error': 'Text too large (max 1MB)'}), 413
        # Create a safe filename from first 24 chars
        base = text.strip().splitlines()[0][:24] or 'clip'
        base = ''.join(ch for ch in base if ch.isalnum() or ch in (' ','-','_')).strip()
        if not base:
            base = 'clip'
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = f"{base}_{ts}.txt"
        # Ensure unique
        path = os.path.join(UPLOADS_DIR, fname)
        i = 1
        while os.path.exists(path):
            fname = f"{base}_{ts}_{i}.txt"; path = os.path.join(UPLOADS_DIR, fname); i += 1
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        e = register_entry(path, 'upload')
        print(f"[CLIP] ✓ Registered clip: {e['name']} -> {e['id']}")
        return jsonify({'success': True, 'id': e['id'], 'name': e['name']})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/cache_status', methods=['GET'])
def api_cache_status():
    if not is_request_from_host():
        return jsonify({'error': 'Forbidden'}), 403
    s = _cache_status_dict()
    # Human-readable too
    s_hr = {
        'entries_count': s['entries_count'],
        'shared': f"{s['shared_count']} files, {format_file_size(s['shared_bytes'])}",
        'uploads': f"{s['uploads_count']} files, {format_file_size(s['uploads_bytes'])}",
    }
    return jsonify({'raw': s, 'readable': s_hr})

@app.route('/settings')
def settings_page():
    # Restrict full settings to host PC; remote shows a friendly notice
    if not is_request_from_host():
        return """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>ShareJadPi Settings</title><style>body{margin:0;background:#0f1320;color:#e7ecf3;font-family:ui-sans-serif,system-ui;-webkit-font-smoothing:antialiased} .wrap{max-width:760px;margin:40px auto;padding:20px;background:#14192b;border:1px solid #233046;border-radius:14px} a{color:#a78bfa;text-decoration:none}</style></head>
<body><div class='wrap'><h2>Settings available on host PC only</h2><p>Open this page on the computer running ShareJadPi to view and change settings.</p><p><a href='/'>← Back to Share</a></p></div></body></html>"""
    # simple inline page with expiry config and paths (host only)
    return """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>ShareJadPi Settings</title>
<style>
    :root{--bg:#0f1320;--card:#14192b;--text:#e7ecf3;--muted:#9aa4b2;--border:#233046;--primary:#22c55e;--primary-600:#16a34a;--danger:#ef4444;--shadow:0 10px 30px rgba(0,0,0,.25)}
    *{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 800px at 20% -10%, #1b2140 0%, var(--bg) 40%),radial-gradient(1000px 600px at 100% 0%, #191a2b 0%, transparent 50%);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Arial;color:var(--text);padding:24px}
    .card{background:linear-gradient(180deg,rgba(255,255,255,.03),rgba(255,255,255,.01));border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);max-width:900px;margin:0 auto;padding:20px}
    h1{margin:6px 0 12px 0;font-size:clamp(20px,3.2vw,28px)}.status{margin:10px 0;font-weight:700;color:var(--muted)}
    fieldset{border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin-top:14px;background:rgba(255,255,255,.02)}legend{padding:0 8px;font-weight:800;color:#cbd5e1}
    button{background:linear-gradient(180deg,var(--primary),var(--primary-600));border:1px solid rgba(255,255,255,.1);color:#08140d;padding:9px 14px;border-radius:10px;cursor:pointer;font-weight:800;font-size:14px;box-shadow:0 6px 18px rgba(34,197,94,.25)}
    button.off{background:#475569;color:#e2e8f0;border-color:#334155}
    button:hover{filter:brightness(1.05)}button:active{transform:translateY(1px)}
    input[type=number]{width:130px;padding:8px;border:1px solid #2a3550;border-radius:10px;background:#0b0f1a;color:var(--text)}
    .mono{font-family:Consolas,Menlo,monospace;word-break:break-all;background:#0b0f1a;padding:6px 8px;border-radius:8px;border:1px solid var(--border);color:#cbd5e1}
    .row{display:flex;gap:8px;flex-wrap:wrap}
    a{color:#a78bfa;text-decoration:none}a:hover{text-decoration:underline}
    @media (max-width:600px){body{padding:16px}.card{padding:14px}}
</style>
<script>
async function refresh(){
  const r=await fetch('/api/autostart');
  const d=await r.json();
  document.getElementById('state').textContent=d.enabled?'Enabled':'Disabled';
  document.getElementById('btnOn').disabled=d.enabled;
  document.getElementById('btnOff').disabled=!d.enabled;
  const re=await fetch('/api/expiry');
  const de=await re.json();
  document.getElementById('expState').textContent=de.enabled? (de.minutes + ' min') : 'Disabled';
  document.getElementById('expiryMinutes').value = de.enabled ? de.minutes : '';
  try{
    const rp=await fetch('/api/paths');
    if(rp.ok){
      const p=await rp.json();
      document.getElementById('coreDir').textContent=p.core;
      document.getElementById('sharedDir').textContent=p.shared;
      document.getElementById('uploadsDir').textContent=p.uploads;
      document.getElementById('pathsNote').style.display='none';
      document.getElementById('pathsBlock').style.display='block';
    }else{
      document.getElementById('pathsNote').style.display='block';
      document.getElementById('pathsBlock').style.display='none';
    }
  }catch(e){
    document.getElementById('pathsNote').style.display='block';
    document.getElementById('pathsBlock').style.display='none';
  }
  // Cache status
  try{
    const rc=await fetch('/api/cache_status');
    if(rc.ok){
      const c=await rc.json();
      document.getElementById('entriesCount').textContent=c.raw.entries_count;
      document.getElementById('sharedStat').textContent=c.readable.shared;
      document.getElementById('uploadsStat').textContent=c.readable.uploads;
      document.getElementById('cacheBlock').style.display='block';
    }
  }catch(e){}
}
async function setAuto(v){await fetch('/api/autostart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({enable:v})});refresh();}
async function applyExpiry(){
  const raw=document.getElementById('expiryMinutes').value.trim();
  let minutes=parseInt(raw,10);
  if(isNaN(minutes)||minutes<=0){minutes=0;}
  await fetch('/api/expiry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({minutes:minutes})});
  refresh();
}
function copyText(elId){
  const t=document.getElementById(elId).textContent;
  navigator.clipboard.writeText(t).then(()=>{
    const btn=document.getElementById(elId+'Btn');
    if(btn){const old=btn.textContent;btn.textContent='Copied';setTimeout(()=>btn.textContent=old,1000);} 
  });
}
async function openPath(which){
  try{
    const r=await fetch('/api/open_path',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which})});
    const d=await r.json();
    if(!r.ok||!d.success){alert('Failed to open: '+(d.error||r.status));}
  }catch(e){alert('Failed to open: '+e);}
}
async function clearCache(){
  const msg=document.getElementById('cacheMsg');
  msg.textContent='';
  const res=await fetch('/api/clear',{method:'POST'});
  const data=await res.json();
  if(data.success){
    if(data.errors && data.errors.length){
      msg.textContent='Some items could not be deleted immediately: '+data.errors.join('; ');
    } else {
      msg.textContent='Cache cleared.';
    }
  } else { msg.textContent='Clear failed.'; }
  refresh();
}
async function hardReset(){
  const msg=document.getElementById('cacheMsg');
  msg.textContent='';
  const res=await fetch('/api/reset_cache',{method:'POST'});
  const data=await res.json();
  if(data.success){ msg.textContent='Hard reset done.'; } else { msg.textContent='Hard reset had errors: '+(data.errors||[]).join('; ');} 
  refresh();
}
async function recreateDirs(){
  const msg=document.getElementById('cacheMsg');
  msg.textContent='';
  const res=await fetch('/api/recreate_dirs',{method:'POST'});
  const data=await res.json();
  if(data.success){ msg.textContent='Directories ensured.'; } else { msg.textContent='Recreate failed.'; }
  refresh();
}
window.onload=refresh;
</script>
</head><body><div class='card'><h1>Settings</h1>
<fieldset><legend>Autostart</legend>
    <div class='status'>State: <span id='state'>...</span></div>
    <div class='row'><button id='btnOn' onclick='setAuto(true)'>Enable Autostart</button> <button class='off' id='btnOff' onclick='setAuto(false)'>Disable Autostart</button></div>
</fieldset>
<fieldset><legend>Automatic Expiry</legend>
    <div class='status'>Current: <span id='expState'>...</span></div>
    <div class='row' style='align-items:center'>
        <label>Minutes (blank/0 = disable): <input type='number' id='expiryMinutes' min='0' step='1' placeholder='0'></label>
        <button onclick='applyExpiry()'>Apply</button>
    </div>
    <p style='font-size:12px;color:#aab1bd;margin-top:8px'>When enabled, entries older than the specified minutes are automatically purged every minute. Copy/zip/upload files are deleted once expired.</p>
</fieldset>
<fieldset><legend>Data Folder (this PC)</legend>
    <p id='pathsNote' style='font-size:12px;color:#aab1bd'>Open this page on the PC running ShareJadPi to see paths.</p>
    <div id='pathsBlock' style='display:none'>
        <div class='row'><strong>Core:</strong> <span id='coreDir' class='mono' style='flex:1'></span> <button id='coreDirBtn' onclick="copyText('coreDir')">Copy</button> <button onclick="openPath('core')">Open</button></div>
        <div class='row' style='margin-top:6px'><strong>Shared:</strong> <span id='sharedDir' class='mono' style='flex:1'></span> <button id='sharedDirBtn' onclick="copyText('sharedDir')">Copy</button> <button onclick="openPath('shared')">Open</button></div>
        <div class='row' style='margin-top:6px'><strong>Uploads:</strong> <span id='uploadsDir' class='mono' style='flex:1'></span> <button id='uploadsDirBtn' onclick="copyText('uploadsDir')">Copy</button> <button onclick="openPath('uploads')">Open</button></div>
        <p style='font-size:12px;color:#aab1bd;margin-top:8px'>Tip: Press Win+R, paste a path, and press Enter to open it in Explorer.</p>
    </div>
</fieldset>
<fieldset id='cacheBlock' style='display:none'><legend>Cache Status</legend>
    <div class='status'>Registry entries: <span id='entriesCount'>...</span></div>
    <div class='status'>Shared dir: <span id='sharedStat'>...</span></div>
    <div class='status'>Uploads dir: <span id='uploadsStat'>...</span></div>
    <div class='row'>
        <button onclick='clearCache()'>Clear Cache (All)</button>
        <button onclick='hardReset()' title='Delete shared/uploads folders and recreate'>Hard Reset</button>
        <button onclick='recreateDirs()' title='Recreate missing folders'>Recreate Dirs</button>
        <button onclick='refresh()'>Rescan</button>
    </div>
  <div id='cacheMsg' style='font-size:12px;color:#555;margin-top:8px'></div>
</fieldset>
<p style='margin-top:24px'><a href='/'>&larr; Back to Share Page</a></p></div></body></html>"""

@app.route('/api/share', methods=['POST'])
def api_share():
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json(silent=True) or {}
    path = data.get('path')
    if not path:
        return jsonify({'error': 'Missing path'}), 400
    if not os.path.exists(path):
        return jsonify({'error': 'Path does not exist'}), 404
    created = share_file_or_folder(path)
    return jsonify({'shared': [ {'id':e['id'], 'name':e['name'], 'kind':e['kind'], 'size': format_file_size(e['size']) } for e in created ], 'count': len(created)})

@app.route('/api/open_path', methods=['POST'])
def api_open_path():
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json(silent=True) or {}
    which = str(data.get('which') or '').lower()
    mapping = {
        'core': CORE_DIR,
        'shared': SHARED_DIR,
        'uploads': UPLOADS_CORE_DIR,
    }
    if which not in mapping:
        return jsonify({'error': 'Invalid which; use core/shared/uploads'}), 400
    path = mapping[which]
    try:
        # Ensure dir exists
        os.makedirs(path, exist_ok=True)
        # Open in Explorer
        os.startfile(path)  # type: ignore[attr-defined]
        return jsonify({'success': True, 'opened': path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'path': path}), 500

@app.route('/api/reset_cache', methods=['POST'])
def api_reset_cache():
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return jsonify({'error': 'Forbidden'}), 403
    errs = []
    # Remove directories completely
    for d in (SHARED_DIR, UPLOADS_CORE_DIR):
        try:
            if os.path.isdir(d):
                shutil.rmtree(d, ignore_errors=True)
        except Exception as e:
            errs.append(f"rmtree {d}: {e}")
    ensure_core_dirs()
    after = _cache_status_dict()
    return jsonify({'success': len(errs)==0, 'errors': errs, 'after': after})

@app.route('/api/recreate_dirs', methods=['POST'])
def api_recreate_dirs():
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return jsonify({'error': 'Forbidden'}), 403
    ensure_core_dirs()
    return jsonify({'success': True, 'paths': {'core': CORE_DIR, 'shared': SHARED_DIR, 'uploads': UPLOADS_CORE_DIR}})

@app.route('/api/speedtest/down')
def speedtest_down():
    # Stream N bytes as fast as possible
    try:
        n = int(request.args.get('bytes', '10485760'))  # default 10MB
    except ValueError:
        n = 10485760
    chunk = b'0' * (256 * 1024)
    def generate():
        remaining = n
        while remaining > 0:
            to_send = chunk if remaining >= len(chunk) else chunk[:remaining]
            yield to_send
            remaining -= len(to_send)
    return app.response_class(generate(), mimetype='application/octet-stream')

@app.route('/api/speedtest/up', methods=['POST'])
def speedtest_up():
    # Accept upload data and discard it (just measure upload speed)
    try:
        # Read all data from request body to measure upload speed
        total_bytes = 0
        chunk_size = 1024 * 1024  # 1MB chunks
        while True:
            chunk = request.stream.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
        return jsonify({'ok': True, 'bytes': total_bytes}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    token = request.cookies.get('sjk') or request.headers.get('X-Auth-Token')
    if token != SECRET_TOKEN:
        abort(403)
    # Expect a set of files with webkitdirectory-style names (path info)
    files = []
    # Support both 'files' and 'files[]' field names
    files.extend(request.files.getlist('files'))
    files.extend(request.files.getlist('files[]'))
    # Also consider any other keys (browser quirks)
    if not files:
        for key in request.files:
            files.extend(request.files.getlist(key))
    folder_name = request.form.get('folder_name') or f"folder_{int(time.time())}"
    if not files:
        return jsonify({'error': 'No files provided'}), 400
    # Stage into a temp folder before zipping
    staging_dir = os.path.join(UPLOADS_CORE_DIR, f"staging_{uuid.uuid4().hex}")
    os.makedirs(staging_dir, exist_ok=True)

    total_bytes = 0
    file_count = 0
    for f in files:
        # Each file has f.filename as a relative path like sub/dir/file.txt
        rel_path = (getattr(f, 'filename', '') or '').replace('\\', '/')
        # Ignore empty folder markers
        if not rel_path or rel_path.endswith('/'):
            continue
        dst_path = os.path.join(staging_dir, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        # Stream to disk
        with open(dst_path, 'wb') as out:
            while True:
                chunk = f.stream.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                total_bytes += len(chunk)
        file_count += 1

    # Prepare zip destination path
    safe_name = re.sub(r'[^A-Za-z0-9._-]+', '_', folder_name).strip('_') or f"folder_{int(time.time())}"
    # Ensure unique zip name
    base_zip = f"{safe_name}.zip"
    zip_path = os.path.join(SHARED_DIR, base_zip)
    if os.path.exists(zip_path):
        i = 1
        while True:
            candidate = os.path.join(SHARED_DIR, f"{safe_name}_{i}.zip")
            if not os.path.exists(candidate):
                zip_path = candidate
                break
            i += 1

    # Create job and launch background worker
    job_id = uuid.uuid4().hex
    with ZIP_JOBS_LOCK:
        ZIP_JOBS[job_id] = {
            'id': job_id,
            'status': 'running',
            'folder_name': safe_name,
            'staging_dir': staging_dir,
            'zip_path': zip_path,
            'total_bytes': total_bytes,
            'processed_bytes': 0,
            'files_total': file_count,
            'files_done': 0,
            'started_at': time.time()
        }
    t = threading.Thread(target=_zip_job_worker, args=(job_id, staging_dir, zip_path), daemon=True)
    t.start()

    # Return 202 with job id for client-side polling
    return jsonify({'ok': True, 'job_id': job_id}), 202

@app.route('/api/is_host')
def api_is_host():
    client_ip = request.remote_addr or ''
    is_host = client_ip in _get_all_local_ips()
    return jsonify({'host': is_host})

def is_request_from_host() -> bool:
    """Return True if the current request originates from the host machine.
    Recognizes loopback and all local interface IPs (IPv4/IPv6).
    """
    try:
        client_ip = request.remote_addr or ''
        return client_ip in _get_all_local_ips()
    except Exception:
        # Fail closed (treat as not host) to be safe
        return False

def run_flask():
    """Run Flask server"""
    # Suppress werkzeug (request) logs to avoid spam from polling
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)

def main():
    # Fast CLI verbs (context menu management and file sharing)
    if len(sys.argv) > 1 and sys.argv[1] == "share":
        if len(sys.argv) > 2:
            file_path = sys.argv[2]
            # Check if server is running
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', PORT))
                s.close()
                # Send request to running server instead of local share
                try:
                    import json as _json, urllib.request as _ur
                    payload = _json.dumps({'path': file_path}).encode()
                    req = _ur.Request(f'http://127.0.0.1:{PORT}/api/share', data=payload, headers={'Content-Type': 'application/json'})
                    with _ur.urlopen(req, timeout=10) as resp:
                        body = resp.read().decode('utf-8', errors='ignore')
                        print("[SHARE] Server response:", body)
                except Exception as e:
                    print(f"[ERROR] Failed to instruct running server to share: {e}")
                    print("Ensure the server is running, then retry.")
                time.sleep(2)
            except Exception:
                print("\n[ERROR] ShareJadPi server is not running!")
                print("Please start the server first by running: python sharejadpi.py")
                print("\nPress Enter to exit...")
                try:
                    input()
                except Exception:
                    pass
            finally:
                try:
                    s.close()
                except Exception:
                    pass
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in ("install-context-menu", "uninstall-context-menu"):
        action = sys.argv[1]
        if action == "install-context-menu":
            ok = install_context_menu_user()
            print(f"[CTX] install (user) -> {'OK' if ok else 'FAILED'}")
        else:
            ok = uninstall_context_menu_user()
            print(f"[CTX] uninstall (user) -> {'OK' if ok else 'FAILED'}")
        sys.exit(0)
    
    # Start server mode
    url = get_access_url(with_token=True)
    
    # Generate initial QR code
    generate_qr_code(url)
    
    print("\n" + "="*60)
    print("🚀 ShareJadPi - Local File Sharing Server")
    print("="*60)
    print(f"\n📱 Access from mobile: {url}")
    print(f"💻 Access from this PC: http://127.0.0.1:{PORT}/?k={SECRET_TOKEN}")
    try:
        ips = sorted([ip for ip in _get_all_local_ips() if ':' not in ip])
        print("\n🌐 Detected local IPv4s:")
        for ip in ips:
            print(f"   - http://{ip}:{PORT}")
    except Exception:
        pass
    print(f"\n✅ Server is running!")
    # Show key paths to help user find data folder
    print("\n📂 Data folders:")
    print(f"   Core   : {CORE_DIR}")
    print(f"   Shared : {SHARED_DIR}")
    print(f"   Uploads: {UPLOADS_CORE_DIR}")
    print("="*60)
    print("\n📋 Tips:")
    print("• Right-click any file/folder → 'Share with ShareJadPi'")
    print("• If the menu isn't there, right-click the tray icon → Install Context Menu")
    print("• A QR popup appears when you share – scan it with your phone")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Start Flask server
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Ensure context menu installed for current user (first run convenience)
    try:
        if platform.system() == 'Windows' and winreg and not context_menu_installed_user():
            ok = install_context_menu_user()
            print(f"[CTX] First-run install -> {'OK' if ok else 'FAILED'}")
    except Exception as _e:
        pass

    # Enable autostart by default on first run (Windows)
    try:
        if platform.system() == 'Windows' and winreg and not is_autostart_enabled():
            if enable_autostart():
                print("[AUTOSTART] Enabled at first run")
    except Exception:
        pass

    # Start tray icon
    tray_thread = threading.Thread(target=start_tray, daemon=True)
    tray_thread.start()

    # Start expiry cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
    cleanup_thread.start()
    
    # Do not auto-open browser; tray provides quick actions
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[STOP] Server stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
