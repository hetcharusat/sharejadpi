#!/usr/bin/env python3
"""
ShareJadPi Development Server
==============================
Development version for testing and local development.
Clean file sharing without advanced features.

Usage:
    python sharejadpi-dev.py                    # Start on port 5000
    python sharejadpi-dev.py --port 8080        # Custom port
    python sharejadpi-dev.py --no-browser       # Don't auto-open browser
"""

import os
import sys
import socket
import webbrowser
import threading
import time
import argparse
import mimetypes
from datetime import datetime
from functools import wraps

# Flask imports
try:
    from flask import Flask, request, send_file, jsonify, make_response
    from werkzeug.utils import secure_filename
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Run: pip install flask werkzeug")
    sys.exit(1)

# Version
APP_VERSION = "4.5.4-dev"

# ============================================================================
# CONFIGURATION
# ============================================================================

UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'ShareJadPi-Dev', 'uploads')
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = 'dev-secret-key'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def format_size(size_bytes):
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower().replace('.', '').upper() or 'FILE'

def get_file_list():
    """Get list of uploaded files"""
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'size_formatted': format_size(stat.st_size),
                    'ext': get_file_extension(filename),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
    return sorted(files, key=lambda x: x['name'].lower())

# ============================================================================
# HTML TEMPLATE (Matches main ShareJadPi UI style)
# ============================================================================

def get_html_template():
    ip = get_local_ip()
    files = get_file_list()
    total_size = sum(f['size'] for f in files)
    
    file_items_html = ""
    if files:
        for f in files:
            file_items_html += f'''
            <div class="file-item" data-name="{f['name']}">
                <div class="file-icon">{f['ext'][:4]}</div>
                <div class="file-info">
                    <div class="file-name">{f['name']}</div>
                    <div class="file-meta">{f['size_formatted']} • {f['modified']}</div>
                </div>
                <div class="file-actions">
                    <button class="file-btn" onclick="downloadFile('{f['name']}')">⬇ Download</button>
                    <button class="file-btn danger" onclick="deleteFile('{f['name']}')">🗑 Delete</button>
                </div>
            </div>'''
    else:
        file_items_html = '''
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <p>No files uploaded yet</p>
                <p class="muted">Drop files above or click to browse</p>
            </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0f1320">
    <title>ShareJadPi Dev - Local File Sharing</title>
    <style>
        :root {{
            --bg: #0f1320;
            --card: #14192b;
            --text: #e7ecf3;
            --muted: #9aa4b2;
            --border: #233046;
            --primary: #22c55e;
            --primary-600: #16a34a;
            --danger: #ef4444;
            --warning: #f59e0b;
            --blue: #3b82f6;
            --purple: #a78bfa;
            --shadow: 0 10px 30px rgba(0,0,0,.25);
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: radial-gradient(1200px 800px at 20% -10%, #1b2140 0%, var(--bg) 40%),
                        radial-gradient(1000px 600px at 100% 0%, #191a2b 0%, transparent 50%);
            color: var(--text);
            -webkit-font-smoothing: antialiased;
            min-height: 100vh;
            padding: 12px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }}
        
        .header h1 {{
            font-size: clamp(20px, 4vw, 28px);
            background: linear-gradient(135deg, var(--primary), var(--blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header-right {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .badge {{
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        
        .badge.connected {{
            background: linear-gradient(135deg, var(--primary), var(--primary-600));
            color: #08140d;
            box-shadow: 0 4px 12px rgba(34,197,94,.3);
        }}
        
        .network-info {{
            font-size: 13px;
            color: var(--muted);
            background: rgba(0,0,0,.3);
            padding: 8px 12px;
            border-radius: 8px;
        }}
        
        .network-info code {{
            color: var(--primary);
            font-weight: 600;
        }}
        
        /* Upload Section */
        .upload-section {{
            background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}
        
        .drag-drop-zone {{
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 16px;
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        .drag-drop-zone.drag-over {{
            border-color: var(--primary);
            background: rgba(34,197,94,.1);
            transform: scale(1.02);
        }}
        
        .drag-drop-zone h3 {{
            font-size: 18px;
            color: var(--text);
            margin-bottom: 8px;
        }}
        
        .drag-drop-zone p {{
            font-size: 14px;
            color: var(--muted);
        }}
        
        .drag-drop-zone .drop-icon {{
            font-size: 48px;
            margin-bottom: 12px;
        }}
        
        .upload-btn {{
            background: linear-gradient(180deg, var(--primary), var(--primary-600));
            border: 1px solid rgba(255,255,255,.1);
            color: #08140d;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 700;
            font-size: 14px;
            transition: all 0.2s;
            box-shadow: 0 6px 18px rgba(34,197,94,.25);
        }}
        
        .upload-btn:hover {{
            filter: brightness(1.05);
            transform: translateY(-2px);
        }}
        
        input[type="file"] {{
            display: none;
        }}
        
        /* Progress */
        .progress-container {{
            display: none;
            margin-top: 16px;
            padding: 16px;
            background: rgba(255,255,255,.02);
            border-radius: 10px;
            border: 1px solid var(--border);
        }}
        
        .progress-container.show {{
            display: block;
        }}
        
        .progress-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .progress-title {{
            font-size: 14px;
            font-weight: 600;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 12px;
            background: rgba(255,255,255,.1);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 8px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--blue));
            transition: width 0.3s;
            width: 0%;
            position: relative;
            overflow: hidden;
        }}
        
        .progress-fill::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.3), transparent);
            animation: shimmer 2s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .progress-text {{
            font-size: 12px;
            color: var(--muted);
            text-align: center;
        }}
        
        /* Files Section */
        .files-section {{
            background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            box-shadow: var(--shadow);
        }}
        
        .files-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .files-header h2 {{
            font-size: 20px;
        }}
        
        .files-stats {{
            font-size: 13px;
            color: var(--muted);
        }}
        
        .file-list {{
            display: grid;
            gap: 10px;
        }}
        
        .file-item {{
            background: rgba(255,255,255,.02);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s;
        }}
        
        .file-item:hover {{
            background: rgba(255,255,255,.05);
            border-color: rgba(255,255,255,.15);
        }}
        
        .file-icon {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--primary), var(--blue));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 11px;
            color: white;
            flex-shrink: 0;
        }}
        
        .file-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .file-name {{
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 4px;
            word-break: break-word;
        }}
        
        .file-meta {{
            font-size: 12px;
            color: var(--muted);
        }}
        
        .file-actions {{
            display: flex;
            gap: 8px;
        }}
        
        .file-btn {{
            padding: 8px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: rgba(255,255,255,.05);
            color: var(--text);
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s;
        }}
        
        .file-btn:hover {{
            background: rgba(255,255,255,.1);
            border-color: rgba(255,255,255,.2);
        }}
        
        .file-btn.danger {{
            color: var(--danger);
        }}
        
        .file-btn.danger:hover {{
            background: rgba(239,68,68,.2);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: var(--muted);
        }}
        
        .empty-state .empty-icon {{
            font-size: 64px;
            margin-bottom: 16px;
            opacity: 0.5;
        }}
        
        .empty-state .muted {{
            font-size: 13px;
            opacity: 0.7;
        }}
        
        /* Toast Notifications */
        .toast {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--card);
            border: 1px solid var(--border);
            padding: 14px 20px;
            border-radius: 10px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s;
            z-index: 1000;
            max-width: 300px;
        }}
        
        .toast.show {{
            transform: translateY(0);
            opacity: 1;
        }}
        
        .toast.success {{
            border-left: 4px solid var(--primary);
        }}
        
        .toast.error {{
            border-left: 4px solid var(--danger);
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: var(--muted);
            font-size: 13px;
        }}
        
        .footer a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .file-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            .file-actions {{
                width: 100%;
            }}
            .file-actions button {{
                flex: 1;
            }}
            .header {{
                flex-direction: column;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div>
                <h1>📁 ShareJadPi Dev</h1>
            </div>
            <div class="header-right">
                <span class="badge connected">● Online</span>
                <div class="network-info">
                    <code>http://{ip}:5000</code>
                </div>
            </div>
        </div>
        
        <!-- Upload Section -->
        <div class="upload-section">
            <div class="drag-drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
                <div class="drop-icon">📂</div>
                <h3>Drop files here to upload</h3>
                <p>or click to browse your files</p>
            </div>
            <div style="text-align: center;">
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                    📤 Select Files
                </button>
            </div>
            <input type="file" id="fileInput" multiple>
            
            <div class="progress-container" id="progressContainer">
                <div class="progress-header">
                    <span class="progress-title" id="progressTitle">Uploading...</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">0%</div>
            </div>
        </div>
        
        <!-- Files Section -->
        <div class="files-section">
            <div class="files-header">
                <h2>📁 Files</h2>
                <span class="files-stats">{len(files)} files • {format_size(total_size)}</span>
            </div>
            <div class="file-list" id="fileList">
                {file_items_html}
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            ShareJadPi Dev v{APP_VERSION} • 
            <a href="https://github.com/hetcharusat/sharejadpi" target="_blank">GitHub</a>
        </div>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const progressTitle = document.getElementById('progressTitle');
        const toast = document.getElementById('toast');
        
        // Drag & Drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(e => {{
            dropZone.addEventListener(e, ev => {{ ev.preventDefault(); ev.stopPropagation(); }});
            document.body.addEventListener(e, ev => {{ ev.preventDefault(); ev.stopPropagation(); }});
        }});
        
        dropZone.addEventListener('dragover', () => dropZone.classList.add('drag-over'));
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
        dropZone.addEventListener('drop', (e) => {{
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
        }});
        
        fileInput.addEventListener('change', () => {{
            if (fileInput.files.length) uploadFiles(fileInput.files);
        }});
        
        function showToast(message, type = 'success') {{
            toast.textContent = message;
            toast.className = 'toast ' + type + ' show';
            setTimeout(() => toast.classList.remove('show'), 3000);
        }}
        
        function uploadFiles(files) {{
            const formData = new FormData();
            for (let f of files) formData.append('file', f);
            
            progressContainer.classList.add('show');
            progressFill.style.width = '0%';
            progressText.textContent = '0%';
            progressTitle.textContent = `Uploading ${{files.length}} file(s)...`;
            
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload');
            
            xhr.upload.onprogress = (e) => {{
                if (e.lengthComputable) {{
                    const pct = Math.round((e.loaded / e.total) * 100);
                    progressFill.style.width = pct + '%';
                    progressText.textContent = pct + '%';
                }}
            }};
            
            xhr.onload = () => {{
                progressContainer.classList.remove('show');
                fileInput.value = '';
                if (xhr.status === 200) {{
                    showToast('✓ Upload successful!', 'success');
                    setTimeout(() => location.reload(), 500);
                }} else {{
                    showToast('✗ Upload failed', 'error');
                }}
            }};
            
            xhr.onerror = () => {{
                progressContainer.classList.remove('show');
                showToast('✗ Upload failed', 'error');
            }};
            
            xhr.send(formData);
        }}
        
        function downloadFile(name) {{
            window.location.href = '/download/' + encodeURIComponent(name);
        }}
        
        function deleteFile(name) {{
            if (!confirm('Delete "' + name + '"?')) return;
            
            fetch('/delete/' + encodeURIComponent(name), {{ method: 'DELETE' }})
                .then(r => r.json())
                .then(data => {{
                    if (data.success) {{
                        showToast('✓ File deleted', 'success');
                        setTimeout(() => location.reload(), 500);
                    }} else {{
                        showToast('✗ Delete failed: ' + data.error, 'error');
                    }}
                }})
                .catch(() => showToast('✗ Delete failed', 'error'));
        }}
    </script>
</body>
</html>'''

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    return get_html_template()

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    uploaded = []
    for file in request.files.getlist('file'):
        if file.filename == '':
            continue
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Handle duplicates
        counter = 1
        base, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1
        
        file.save(filepath)
        uploaded.append(filename)
        print(f"[✓] Uploaded: {filename}")
    
    return jsonify({'success': True, 'files': uploaded}), 200

@app.route('/files', methods=['GET'])
def list_files():
    """List all files as JSON"""
    return jsonify({'files': get_file_list()}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file"""
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a file"""
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    os.remove(filepath)
    print(f"[✓] Deleted: {filename}")
    return jsonify({'success': True}), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Server status"""
    files = get_file_list()
    total_size = sum(f['size'] for f in files)
    return jsonify({
        'status': 'running',
        'version': APP_VERSION,
        'files': len(files),
        'total_size': format_size(total_size),
        'upload_folder': UPLOAD_FOLDER
    }), 200

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='ShareJadPi Development Server')
    parser.add_argument('--port', '-p', type=int, default=5000)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--host', default='0.0.0.0')
    args = parser.parse_args()
    
    ip = get_local_ip()
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📁 ShareJadPi Development Server                           ║
║   Version: {APP_VERSION}                                         ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   Local:    http://localhost:{args.port}                          ║
║   Network:  http://{ip}:{args.port}                          ║
║                                                               ║
║   Upload:   {UPLOAD_FOLDER[:45]:<45} ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    if not args.no_browser:
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{args.port}')
        threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host=args.host, port=args.port, debug=True, threaded=True)

if __name__ == '__main__':
    main()
