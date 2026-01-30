#!/usr/bin/env python3
"""
ShareJadPi Development Server
=============================
Development version with enhanced debugging, hot-reload, and testing features.

Usage:
    python sharejadpi-dev.py                    # Start dev server on port 5000
    python sharejadpi-dev.py --port 8080        # Custom port
    python sharejadpi-dev.py --no-browser       # Don't auto-open browser
    python sharejadpi-dev.py --verbose          # Extra verbose logging

Features:
    - Debug mode enabled (Flask debug=True)
    - Auto-reload on code changes
    - Verbose logging to console
    - CORS enabled for frontend development
    - Mock data for testing
    - Performance metrics
"""

import os
import sys
import socket
import secrets
import urllib.parse
import webbrowser
import threading
import time
import json
import logging
import argparse
from datetime import datetime
from functools import wraps

# Add color support for Windows
if sys.platform == 'win32':
    os.system('color')

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg):
    print(f"{Colors.CYAN}[INFO]{Colors.ENDC} {msg}")

def log_success(msg):
    print(f"{Colors.GREEN}[OK]{Colors.ENDC} {msg}")

def log_warning(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} {msg}")

def log_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.ENDC} {msg}")

def log_debug(msg):
    if VERBOSE:
        print(f"{Colors.BLUE}[DEBUG]{Colors.ENDC} {msg}")

# Global verbose flag
VERBOSE = False

# Version
DEV_VERSION = "4.5.4-dev"

# Flask imports
try:
    from flask import Flask, render_template, request, send_file, jsonify, send_from_directory, redirect, make_response, g
    from werkzeug.utils import secure_filename
    from flask_cors import CORS
except ImportError as e:
    log_error(f"Missing dependency: {e}")
    log_info("Run: pip install flask flask-cors werkzeug")
    sys.exit(1)

# Optional imports
try:
    import qrcode
    from PIL import Image
    HAS_QR = True
except ImportError:
    HAS_QR = False
    log_warning("qrcode/PIL not installed - QR features disabled")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Development settings
DEV_CONFIG = {
    'DEBUG': True,
    'TESTING': False,
    'SECRET_KEY': 'dev-secret-key-not-for-production',
    'MAX_CONTENT_LENGTH': 500 * 1024 * 1024,  # 500MB max upload in dev
    'UPLOAD_FOLDER': os.path.join(os.path.expanduser('~'), 'ShareJadPi-Dev', 'uploads'),
    'ALLOWED_EXTENSIONS': {'*'},  # Allow all in dev mode
    'CORS_ORIGINS': '*',  # Allow all origins in dev
}

# Ensure upload folder exists
os.makedirs(DEV_CONFIG['UPLOAD_FOLDER'], exist_ok=True)

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

app.config.update(DEV_CONFIG)

# Enable CORS for development
CORS(app, origins=DEV_CONFIG['CORS_ORIGINS'])

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ShareJadPi-Dev')

# ============================================================================
# MIDDLEWARE & DECORATORS
# ============================================================================

def timing_decorator(f):
    """Measure and log request timing"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = (time.time() - start) * 1000
        log_debug(f"{request.method} {request.path} - {duration:.2f}ms")
        return result
    return decorated_function

@app.before_request
def before_request():
    g.start_time = time.time()
    log_debug(f"→ {request.method} {request.path}")

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        duration = (time.time() - g.start_time) * 1000
        response.headers['X-Response-Time'] = f'{duration:.2f}ms'
    
    # Add dev headers
    response.headers['X-ShareJadPi-Version'] = DEV_VERSION
    response.headers['X-Environment'] = 'development'
    
    status_color = Colors.GREEN if response.status_code < 400 else Colors.RED
    log_debug(f"← {status_color}{response.status_code}{Colors.ENDC} ({duration:.2f}ms)")
    
    return response

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

def format_file_size(size_bytes):
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_file_info(filepath):
    """Get detailed file information"""
    stat = os.stat(filepath)
    return {
        'name': os.path.basename(filepath),
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
    }

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
@timing_decorator
def index():
    """Main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        log_error(f"Template error: {e}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ShareJadPi Dev</title>
            <style>
                body {{ font-family: system-ui; background: #1a1a2e; color: #eee; padding: 40px; }}
                h1 {{ color: #00d9ff; }}
                .info {{ background: #16213e; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                code {{ background: #0f3460; padding: 2px 8px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <h1>🚀 ShareJadPi Development Server</h1>
            <div class="info">
                <p><strong>Version:</strong> {DEV_VERSION}</p>
                <p><strong>Status:</strong> Running in development mode</p>
                <p><strong>Upload Folder:</strong> <code>{DEV_CONFIG['UPLOAD_FOLDER']}</code></p>
                <p><strong>Template Error:</strong> <code>{e}</code></p>
            </div>
            <h2>API Endpoints</h2>
            <ul>
                <li><code>POST /upload</code> - Upload a file</li>
                <li><code>GET /files</code> - List all files</li>
                <li><code>GET /download/&lt;filename&gt;</code> - Download a file</li>
                <li><code>DELETE /delete/&lt;filename&gt;</code> - Delete a file</li>
                <li><code>GET /api/status</code> - Server status</li>
            </ul>
        </body>
        </html>
        """, 200

@app.route('/upload', methods=['POST'])
@timing_decorator
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided', 'code': 'MISSING_FILE'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected', 'code': 'EMPTY_FILENAME'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(DEV_CONFIG['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames
        counter = 1
        base, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(DEV_CONFIG['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        file_info = get_file_info(filepath)
        
        log_success(f"Uploaded: {filename} ({file_info['size_formatted']})")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': file_info['size'],
            'size_formatted': file_info['size_formatted'],
            'upload_time': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        log_error(f"Upload failed: {e}")
        return jsonify({'error': str(e), 'code': 'UPLOAD_ERROR'}), 500

@app.route('/files', methods=['GET'])
@timing_decorator
def list_files():
    """List all uploaded files"""
    try:
        files = []
        upload_dir = DEV_CONFIG['UPLOAD_FOLDER']
        
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                filepath = os.path.join(upload_dir, filename)
                if os.path.isfile(filepath):
                    files.append(get_file_info(filepath))
        
        return jsonify({
            'files': files,
            'total': len(files),
            'upload_folder': upload_dir
        }), 200
        
    except Exception as e:
        log_error(f"List files failed: {e}")
        return jsonify({'error': str(e), 'code': 'LIST_ERROR'}), 500

@app.route('/download/<filename>', methods=['GET'])
@timing_decorator
def download_file(filename):
    """Download a file"""
    try:
        filepath = os.path.join(DEV_CONFIG['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found', 'code': 'FILE_NOT_FOUND'}), 404
        
        log_info(f"Download: {filename}")
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        log_error(f"Download failed: {e}")
        return jsonify({'error': str(e), 'code': 'DOWNLOAD_ERROR'}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
@timing_decorator
def delete_file(filename):
    """Delete a file"""
    try:
        filepath = os.path.join(DEV_CONFIG['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found', 'code': 'FILE_NOT_FOUND'}), 404
        
        os.remove(filepath)
        log_success(f"Deleted: {filename}")
        
        return jsonify({
            'success': True,
            'message': f'File {filename} deleted successfully'
        }), 200
        
    except Exception as e:
        log_error(f"Delete failed: {e}")
        return jsonify({'error': str(e), 'code': 'DELETE_ERROR'}), 500

@app.route('/api/status', methods=['GET'])
@timing_decorator
def api_status():
    """Get server status"""
    upload_dir = DEV_CONFIG['UPLOAD_FOLDER']
    file_count = len([f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]) if os.path.exists(upload_dir) else 0
    
    total_size = 0
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            fp = os.path.join(upload_dir, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    
    return jsonify({
        'status': 'running',
        'version': DEV_VERSION,
        'environment': 'development',
        'debug': app.debug,
        'local_ip': get_local_ip(),
        'upload_folder': upload_dir,
        'file_count': file_count,
        'total_size': total_size,
        'total_size_formatted': format_file_size(total_size),
        'features': {
            'qr_code': HAS_QR,
            'cors': True,
            'max_upload_mb': DEV_CONFIG['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        },
        'uptime': time.time() - START_TIME if 'START_TIME' in globals() else 0
    }), 200

@app.route('/api/qr', methods=['GET'])
@timing_decorator
def generate_qr():
    """Generate QR code for the server URL"""
    if not HAS_QR:
        return jsonify({'error': 'QR code feature not available', 'code': 'QR_DISABLED'}), 501
    
    try:
        import io
        import base64
        
        ip = get_local_ip()
        port = request.host.split(':')[1] if ':' in request.host else '5000'
        url = f"http://{ip}:{port}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'url': url,
            'qr_code': f"data:image/png;base64,{img_str}"
        }), 200
        
    except Exception as e:
        log_error(f"QR generation failed: {e}")
        return jsonify({'error': str(e), 'code': 'QR_ERROR'}), 500

# ============================================================================
# STATIC FILES (development fallback)
# ============================================================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'code': 'NOT_FOUND'}), 404

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        'error': f'File too large. Max size: {DEV_CONFIG["MAX_CONTENT_LENGTH"] / (1024*1024):.0f}MB',
        'code': 'FILE_TOO_LARGE'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    log_error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}), 500

# ============================================================================
# MAIN
# ============================================================================

def print_banner(ip, port):
    """Print startup banner"""
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   {Colors.BOLD}ShareJadPi Development Server{Colors.ENDC}{Colors.CYAN}                              ║
║   Version: {DEV_VERSION}                                          ║
║                                                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                                ║
║   {Colors.GREEN}Local:{Colors.ENDC}{Colors.CYAN}    http://localhost:{port:<5}                           ║
║   {Colors.GREEN}Network:{Colors.ENDC}{Colors.CYAN}  http://{ip}:{port:<5}                         ║
║                                                                ║
║   {Colors.YELLOW}Debug Mode:{Colors.ENDC}{Colors.CYAN} ON                                            ║
║   {Colors.YELLOW}Auto-Reload:{Colors.ENDC}{Colors.CYAN} ON                                           ║
║   {Colors.YELLOW}CORS:{Colors.ENDC}{Colors.CYAN} Enabled (all origins)                              ║
║                                                                ║
║   Upload Folder: {DEV_CONFIG['UPLOAD_FOLDER'][:40]:<40} ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BLUE}Press Ctrl+C to stop the server{Colors.ENDC}
""")

def main():
    global VERBOSE, START_TIME
    
    parser = argparse.ArgumentParser(description='ShareJadPi Development Server')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run on (default: 5000)')
    parser.add_argument('--no-browser', action='store_true', help="Don't auto-open browser")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    
    args = parser.parse_args()
    VERBOSE = args.verbose
    START_TIME = time.time()
    
    ip = get_local_ip()
    port = args.port
    
    print_banner(ip, port)
    
    # Open browser
    if not args.no_browser:
        def open_browser():
            time.sleep(1.5)
            webbrowser.open(f'http://localhost:{port}')
        threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask development server
    try:
        app.run(
            host=args.host,
            port=port,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Server stopped.{Colors.ENDC}")
    except Exception as e:
        log_error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
