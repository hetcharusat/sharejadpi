import os
import socket
import qrcode
from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import webbrowser
from threading import Timer

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'shared_files'
ALLOWED_EXTENSIONS = {'*'}  # Allow all file types
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr_code(url):
    """Generate QR code for the URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = "static/qr_code.png"
    
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    img.save(qr_path)
    return qr_path

@app.route('/')
def index():
    """Main page"""
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            size_str = format_file_size(size)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            files.append({
                'name': filename,
                'size': size_str,
                'modified': modified
            })
    
    # Sort by modified time (newest first)
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or file.filename is None:
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Add timestamp if file already exists
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
    """Handle file download"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Handle file deletion"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/qr')
def qr_code():
    """Serve QR code image"""
    return send_from_directory('static', 'qr_code.png')

def format_file_size(size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    url = f"http://{local_ip}:{port}"
    
    # Generate QR code
    qr_path = generate_qr_code(url)
    
    print("\n" + "="*60)
    print("🚀 ShareJadPi - Local File Sharing Server")
    print("="*60)
    print(f"\n📱 Access from your mobile browser:")
    print(f"   {url}")
    print(f"\n💻 Access from this computer:")
    print(f"   http://127.0.0.1:{port}")
    print(f"\n📷 Scan QR code to connect from mobile!")
    print(f"   QR code saved at: {qr_path}")
    print("\n⚠️  Make sure your mobile and PC are on the same WiFi network!")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser automatically after 1 second
    Timer(1.0, open_browser).start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
