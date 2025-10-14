import os
import sys
import socket
import qrcode
import webbrowser
import threading
import json
from pathlib import Path
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import pystray
from pystray import MenuItem as item
import keyboard
import winreg
import shutil

# Configuration
UPLOAD_FOLDER = 'shared_files'
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
PORT = 5000
HOTKEY = 'ctrl+shift+q'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Global variables
server_running = False
local_ip = None
tray_icon = None

# Create folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

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

def generate_qr_code(url):
    """Generate QR code and return as PIL Image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to static folder as well
    img.save("static/qr_code.png")
    return img

def create_tray_icon():
    """Create a simple icon for system tray"""
    # Create a simple colored square icon
    image = Image.new('RGB', (64, 64), color=(102, 126, 234))
    return image

def show_qr_code(icon, item):
    """Show QR code in browser"""
    webbrowser.open(f'http://127.0.0.1:{PORT}')

def copy_url_to_clipboard(icon, item):
    """Copy URL to clipboard"""
    url = f"http://{local_ip}:{PORT}"
    os.system(f'echo {url} | clip')
    icon.notify("URL copied to clipboard!", "ShareJadPi")

def open_shared_folder(icon, item):
    """Open the shared files folder"""
    os.startfile(os.path.abspath(UPLOAD_FOLDER))

def share_selected_files():
    """Share currently selected files in Explorer"""
    try:
        # Try to use win32clipboard to get selected files
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            try:
                data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                files = list(data)
            except:
                files = []
            finally:
                win32clipboard.CloseClipboard()
        except ImportError:
            # Fallback: notify user to use context menu or drag-drop
            if tray_icon:
                tray_icon.notify("Please use context menu or drag & drop to share files", "ShareJadPi")
            return
        
        if files:
            for file_path in files:
                if os.path.isfile(file_path):
                    filename = os.path.basename(file_path)
                    dest = os.path.join(UPLOAD_FOLDER, filename)
                    # Add timestamp if exists
                    if os.path.exists(dest):
                        name, ext = os.path.splitext(filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{name}_{timestamp}{ext}"
                        dest = os.path.join(UPLOAD_FOLDER, filename)
                    shutil.copy2(file_path, dest)
            
            if tray_icon:
                tray_icon.notify(f"{len(files)} file(s) shared!", "ShareJadPi")
        else:
            if tray_icon:
                tray_icon.notify("No files selected. Select files first, then press the hotkey.", "ShareJadPi")
    except Exception as e:
        print(f"Error sharing files: {e}")
        if tray_icon:
            tray_icon.notify(f"Error: {str(e)}", "ShareJadPi")

def add_to_startup(icon, item):
    """Add ShareJadPi to Windows startup"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        exe_path = os.path.abspath(sys.argv[0])
        winreg.SetValueEx(key, "ShareJadPi", 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)
        icon.notify("Added to startup!", "ShareJadPi")
    except Exception as e:
        icon.notify(f"Failed to add to startup: {e}", "ShareJadPi")

def remove_from_startup(icon, item):
    """Remove ShareJadPi from Windows startup"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "ShareJadPi")
        winreg.CloseKey(key)
        icon.notify("Removed from startup!", "ShareJadPi")
    except:
        pass

def add_context_menu(icon, item):
    """Add 'Share with ShareJadPi' to Windows context menu"""
    try:
        exe_path = os.path.abspath(sys.argv[0])
        
        # For files
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\ShareJadPi")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "📱 Share with ShareJadPi")
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)
        
        command_key = winreg.CreateKey(key, "command")
        winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, f'"{exe_path}" share "%1"')
        winreg.CloseKey(command_key)
        winreg.CloseKey(key)
        
        # For folders
        folder_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\ShareJadPi")
        winreg.SetValueEx(folder_key, "", 0, winreg.REG_SZ, "📱 Share with ShareJadPi")
        winreg.SetValueEx(folder_key, "Icon", 0, winreg.REG_SZ, exe_path)
        
        folder_command_key = winreg.CreateKey(folder_key, "command")
        winreg.SetValueEx(folder_command_key, "", 0, winreg.REG_SZ, f'"{exe_path}" share "%1"')
        winreg.CloseKey(folder_command_key)
        winreg.CloseKey(folder_key)
        
        icon.notify("Context menu added! Right-click any file or folder to share.", "ShareJadPi")
    except Exception as e:
        icon.notify(f"Failed to add context menu: {e}", "ShareJadPi")

def remove_context_menu(icon, item):
    """Remove context menu entry"""
    try:
        # Remove file context menu
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\ShareJadPi\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\ShareJadPi")
        except:
            pass
        
        # Remove folder context menu
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\ShareJadPi\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\ShareJadPi")
        except:
            pass
            
        icon.notify("Context menu removed!", "ShareJadPi")
    except:
        pass

def quit_app(icon, item):
    """Quit the application"""
    icon.stop()
    os._exit(0)

# Flask routes (same as before)
@app.route('/')
def index():
    files = []
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '' or file.filename is None:
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename:
        filename = secure_filename(file.filename)
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename}), 200
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True}), 200
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/qr')
def qr_code():
    return send_from_directory('static', 'qr_code.png')

def format_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def run_flask():
    """Run Flask server in background"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def setup_hotkey():
    """Setup global hotkey"""
    try:
        keyboard.add_hotkey(HOTKEY, share_selected_files)
    except:
        pass

def share_file_or_folder(path):
    """Share a file or folder (called from context menu)"""
    shared_count = 0
    
    try:
        print(f"[DEBUG] Attempting to share: {path}")
        
        if os.path.isfile(path):
            # Share single file
            filename = os.path.basename(path)
            dest = os.path.join(UPLOAD_FOLDER, filename)
            
            print(f"[DEBUG] File detected: {filename}")
            print(f"[DEBUG] Destination: {dest}")
            
            # Add timestamp if exists
            if os.path.exists(dest):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{name}_{timestamp}{ext}"
                dest = os.path.join(UPLOAD_FOLDER, filename)
                print(f"[DEBUG] File exists, renamed to: {filename}")
            
            shutil.copy2(path, dest)
            shared_count = 1
            print(f"[DEBUG] File copied successfully!")
            
        elif os.path.isdir(path):
            # Share all files in folder
            print(f"[DEBUG] Folder detected, sharing all files inside")
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    filename = os.path.basename(item_path)
                    dest = os.path.join(UPLOAD_FOLDER, filename)
                    
                    # Add timestamp if exists
                    if os.path.exists(dest):
                        name, ext = os.path.splitext(filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{name}_{timestamp}{ext}"
                        dest = os.path.join(UPLOAD_FOLDER, filename)
                    
                    shutil.copy2(item_path, dest)
                    shared_count += 1
            print(f"[DEBUG] {shared_count} files copied from folder")
        
        # Show notification with link and instructions
        if shared_count > 0:
            local_ip = get_local_ip()
            url = f"http://{local_ip}:{PORT}"
            
            print(f"[DEBUG] Creating notification...")
            
            # Create a notification with clickable link
            from winotify import Notification, audio
            
            qr_icon_path = os.path.abspath("static/qr_code.png")
            
            if os.path.exists(qr_icon_path):
                toast = Notification(
                    app_id="ShareJadPi",
                    title=f"✅ {shared_count} file(s) shared!",
                    msg=f"Access from mobile:\n{url}\n\nClick to open in browser",
                    duration="long",
                    icon=qr_icon_path
                )
            else:
                toast = Notification(
                    app_id="ShareJadPi",
                    title=f"✅ {shared_count} file(s) shared!",
                    msg=f"Access from mobile:\n{url}\n\nClick to open in browser",
                    duration="long"
                )
            
            toast.set_audio(audio.Default, loop=False)
            toast.add_actions(label="Open Browser", launch=url)
            toast.add_actions(label="Copy Link", launch=f"cmd /c echo {url} | clip")
            toast.show()
            print(f"[DEBUG] Notification sent!")
            
    except Exception as e:
        print(f"[ERROR] Error sharing: {e}")
        import traceback
        traceback.print_exc()

def main():
    global local_ip, tray_icon
    
    # Handle command line file sharing (from context menu)
    if len(sys.argv) > 1:
        if sys.argv[1] == "share":
            # Called from context menu
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                
                # Make sure server is running first
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(('127.0.0.1', PORT))
                    s.close()
                    # Server is running, share the file
                    share_file_or_folder(file_path)
                except:
                    # Server not running, show error
                    from winotify import Notification
                    toast = Notification(
                        app_id="ShareJadPi",
                        title="⚠️ ShareJadPi Not Running",
                        msg="Please start ShareJadPi first!\nLook for the blue icon in system tray.",
                        duration="long"
                    )
                    toast.show()
                finally:
                    s.close()
            sys.exit(0)
    
    # Get local IP and generate QR
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{PORT}"
    generate_qr_code(url)
    
    # Start Flask server in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Create system tray menu
    menu = pystray.Menu(
        item('📱 Show QR Code & Link', show_qr_code, default=True),
        item('📋 Copy URL to Clipboard', copy_url_to_clipboard),
        item('📂 Open Shared Files Folder', open_shared_folder),
        pystray.Menu.SEPARATOR,
        item('➕ Add Context Menu (Right-click files)', add_context_menu),
        item('➖ Remove Context Menu', remove_context_menu),
        pystray.Menu.SEPARATOR,
        item('⚙️ Start with Windows', add_to_startup),
        item('❌ Don\'t Start with Windows', remove_from_startup),
        pystray.Menu.SEPARATOR,
        item(f'🌐 {local_ip}:{PORT}', None, enabled=False),
        pystray.Menu.SEPARATOR,
        item('🚪 Quit', quit_app)
    )
    
    # Create and run system tray icon
    icon_image = create_tray_icon()
    tray_icon = pystray.Icon("ShareJadPi", icon_image, "ShareJadPi", menu)
    
    print(f"\n{'='*60}")
    print("🚀 ShareJadPi - Background Mode")
    print(f"{'='*60}")
    print(f"✅ Server running: http://{local_ip}:{PORT}")
    print(f"� Right-click any file → 'Share with ShareJadPi'")
    print(f"🖱️ Right-click tray icon for QR code and options")
    print(f"{'='*60}\n")
    
    # Show notification
    tray_icon.notify(f"Ready! Right-click files to share.\nServer: {local_ip}:{PORT}", "ShareJadPi Started!")
    
    # Run the tray icon
    tray_icon.run()

if __name__ == '__main__':
    main()
