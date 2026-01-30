#!/usr/bin/env python3
"""
ShareJadPi Development Server (Lite)
=====================================
Clean development version - file sharing only.
No QR codes, no clipboard sync, no token auth, no speed test.

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
from datetime import datetime
from functools import wraps

# Flask imports
try:
    from flask import Flask, request, send_file, jsonify, send_from_directory, make_response
    from werkzeug.utils import secure_filename
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Run: pip install flask werkzeug")
    sys.exit(1)

# Version
DEV_VERSION = "4.5.4-dev-lite"

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
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
    return sorted(files, key=lambda x: x['name'].lower())

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page - simple HTML UI"""
    ip = get_local_ip()
    port = request.host.split(':')[1] if ':' in request.host else '5000'
    files = get_file_list()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShareJadPi Dev</title>
    <style>
        :root {{
            --bg: #0f1320;
            --card: #1a1f35;
            --text: #e7ecf3;
            --muted: #9aa4b2;
            --border: #2a3550;
            --primary: #22c55e;
            --primary-hover: #16a34a;
            --danger: #ef4444;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        
        .header h1 {{
            font-size: 24px;
            background: linear-gradient(135deg, var(--primary), #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header .info {{
            font-size: 14px;
            color: var(--muted);
        }}
        
        .header .info code {{
            background: #0d1117;
            padding: 4px 8px;
            border-radius: 4px;
            color: var(--primary);
        }}
        
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .card h2 {{
            font-size: 18px;
            margin-bottom: 16px;
            color: var(--text);
        }}
        
        /* Upload Zone */
        .upload-zone {{
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .upload-zone:hover, .upload-zone.dragover {{
            border-color: var(--primary);
            background: rgba(34, 197, 94, 0.1);
        }}
        
        .upload-zone p {{
            color: var(--muted);
            margin-bottom: 12px;
        }}
        
        .upload-zone .icon {{
            font-size: 48px;
            margin-bottom: 12px;
        }}
        
        #fileInput {{
            display: none;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        
        .btn-primary {{
            background: var(--primary);
            color: #000;
        }}
        
        .btn-primary:hover {{
            background: var(--primary-hover);
        }}
        
        .btn-danger {{
            background: var(--danger);
            color: #fff;
        }}
        
        .btn-danger:hover {{
            opacity: 0.9;
        }}
        
        /* Progress */
        .progress-container {{
            display: none;
            margin-top: 16px;
        }}
        
        .progress-bar {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--primary);
            width: 0%;
            transition: width 0.3s;
        }}
        
        .progress-text {{
            font-size: 14px;
            color: var(--muted);
            margin-top: 8px;
        }}
        
        /* File List */
        .file-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .file-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 8px;
        }}
        
        .file-info {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
            min-width: 0;
        }}
        
        .file-icon {{
            font-size: 24px;
        }}
        
        .file-name {{
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .file-meta {{
            font-size: 12px;
            color: var(--muted);
        }}
        
        .file-actions {{
            display: flex;
            gap: 8px;
        }}
        
        .file-actions button {{
            padding: 6px 12px;
            font-size: 12px;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: var(--muted);
        }}
        
        .empty-state .icon {{
            font-size: 48px;
            margin-bottom: 12px;
            opacity: 0.5;
        }}
        
        /* Toast */
        .toast {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--card);
            border: 1px solid var(--border);
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s;
            z-index: 1000;
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
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>📁 ShareJadPi Dev</h1>
                <div class="info">Version {DEV_VERSION}</div>
            </div>
            <div class="info">
                Access: <code>http://{ip}:{port}</code>
            </div>
        </div>
        
        <div class="card">
            <h2>📤 Upload Files</h2>
            <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
                <div class="icon">📂</div>
                <p>Drop files here or click to browse</p>
                <button class="btn btn-primary">Select Files</button>
            </div>
            <input type="file" id="fileInput" multiple>
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">Uploading...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📁 Files ({len(files)})</h2>
            <div class="file-list" id="fileList">
                {"".join([f'''
                <div class="file-item" data-name="{f['name']}">
                    <div class="file-info">
                        <span class="file-icon">📄</span>
                        <div>
                            <div class="file-name">{f['name']}</div>
                            <div class="file-meta">{f['size_formatted']} • {f['modified']}</div>
                        </div>
                    </div>
                    <div class="file-actions">
                        <button class="btn btn-primary" onclick="downloadFile('{f['name']}')">Download</button>
                        <button class="btn btn-danger" onclick="deleteFile('{f['name']}')">Delete</button>
                    </div>
                </div>
                ''' for f in files]) if files else '''
                <div class="empty-state">
                    <div class="icon">📭</div>
                    <p>No files uploaded yet</p>
                </div>
                '''}
            </div>
        </div>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const toast = document.getElementById('toast');
        
        // Drag & Drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(e => {{
            uploadZone.addEventListener(e, ev => ev.preventDefault());
        }});
        
        uploadZone.addEventListener('dragover', () => uploadZone.classList.add('dragover'));
        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
        uploadZone.addEventListener('drop', (e) => {{
            uploadZone.classList.remove('dragover');
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
            
            progressContainer.style.display = 'block';
            progressFill.style.width = '0%';
            progressText.textContent = 'Uploading...';
            
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload');
            
            xhr.upload.onprogress = (e) => {{
                if (e.lengthComputable) {{
                    const pct = (e.loaded / e.total) * 100;
                    progressFill.style.width = pct + '%';
                    progressText.textContent = `Uploading: ${{pct.toFixed(0)}}%`;
                }}
            }};
            
            xhr.onload = () => {{
                progressContainer.style.display = 'none';
                if (xhr.status === 200) {{
                    showToast('Upload successful!', 'success');
                    location.reload();
                }} else {{
                    showToast('Upload failed: ' + xhr.statusText, 'error');
                }}
            }};
            
            xhr.onerror = () => {{
                progressContainer.style.display = 'none';
                showToast('Upload failed', 'error');
            }};
            
            xhr.send(formData);
        }}
        
        function downloadFile(name) {{
            window.location.href = '/download/' + encodeURIComponent(name);
        }}
        
        function deleteFile(name) {{
            if (!confirm('Delete ' + name + '?')) return;
            
            fetch('/delete/' + encodeURIComponent(name), {{ method: 'DELETE' }})
                .then(r => r.json())
                .then(data => {{
                    if (data.success) {{
                        showToast('File deleted', 'success');
                        location.reload();
                    }} else {{
                        showToast('Delete failed: ' + data.error, 'error');
                    }}
                }})
                .catch(() => showToast('Delete failed', 'error'));
        }}
    </script>
</body>
</html>'''
    return html

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
        print(f"[OK] Uploaded: {filename}")
    
    return jsonify({'success': True, 'files': uploaded}), 200

@app.route('/files', methods=['GET'])
def list_files():
    """List all files"""
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
    print(f"[OK] Deleted: {filename}")
    return jsonify({'success': True}), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Server status"""
    files = get_file_list()
    total_size = sum(f['size'] for f in files)
    return jsonify({
        'status': 'running',
        'version': DEV_VERSION,
        'files': len(files),
        'total_size': format_size(total_size),
        'upload_folder': UPLOAD_FOLDER
    }), 200

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='ShareJadPi Dev Server (Lite)')
    parser.add_argument('--port', '-p', type=int, default=5000)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--host', default='0.0.0.0')
    args = parser.parse_args()
    
    ip = get_local_ip()
    
    print(f"""
╔═══════════════════════════════════════════════════════╗
║  ShareJadPi Dev Server (Lite) v{DEV_VERSION}        ║
╠═══════════════════════════════════════════════════════╣
║  Local:   http://localhost:{args.port}                    ║
║  Network: http://{ip}:{args.port}                    ║
║  Upload:  {UPLOAD_FOLDER[:40]:<40} ║
╚═══════════════════════════════════════════════════════╝
""")
    
    if not args.no_browser:
        threading.Thread(target=lambda: (time.sleep(1), webbrowser.open(f'http://localhost:{args.port}')), daemon=True).start()
    
    app.run(host=args.host, port=args.port, debug=True, threaded=True)

if __name__ == '__main__':
    main()
