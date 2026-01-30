# 🏗️ System Architecture

<div class="arch-hero">
  <h2>Under the Hood of ShareJadPi</h2>
  <p>A deep dive into the technical architecture, design patterns, and system components that power ShareJadPi.</p>
</div>

## 🎯 Architecture Overview

ShareJadPi follows a **monolithic architecture** optimized for simplicity and performance. A single Python application handles everything from HTTP routing to file management.

```mermaid
flowchart TB
    subgraph Presentation["🎨 Presentation Layer"]
        direction LR
        HTML["HTML Templates"]
        CSS["CSS Styling"]
        JS["JavaScript"]
    end
    
    subgraph Application["⚡ Application Layer"]
        direction TB
        Flask["Flask App"]
        Routes["Route Handlers"]
        Middleware["Middleware"]
    end
    
    subgraph Business["🧠 Business Logic"]
        direction TB
        FileManager["File Manager"]
        AuthManager["Auth Manager"]
        ShareManager["Share Manager"]
        CloudflareManager["Cloudflare Manager"]
    end
    
    subgraph Infrastructure["🔧 Infrastructure"]
        direction LR
        FileSystem["File System"]
        Config["Configuration"]
        Cache["In-Memory Cache"]
    end
    
    subgraph External["🌐 External Services"]
        Cloudflare["Cloudflare Tunnel"]
    end
    
    Presentation --> Application
    Application --> Business
    Business --> Infrastructure
    Business --> External
    
    style Presentation fill:#581c87,stroke:#a855f7,color:#fff
    style Application fill:#065f46,stroke:#10b981,color:#fff
    style Business fill:#1e40af,stroke:#3b82f6,color:#fff
    style Infrastructure fill:#7c2d12,stroke:#f97316,color:#fff
    style External fill:#166534,stroke:#22c55e,color:#fff
```

---

## 📁 Project Structure

```
sharejadpi/
├── 📄 sharejadpi.py          # Main application (3000+ lines)
├── 📄 requirements.txt       # Python dependencies
├── 📁 templates/             # HTML templates
│   └── index.html           # Main UI template
├── 📁 static/                # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── 📁 SGP_phase1/            # Development tools
│   ├── sharejadpi-dev.py    # Dev server
│   └── docs/                # This documentation
├── 📁 build_tools/           # Build configurations
│   ├── *.spec               # PyInstaller specs
│   └── *.iss                # Installer scripts
└── 📁 scripts/               # Utility scripts
    ├── fix_firewall.ps1
    └── show_connection_info.ps1
```

---

## 🔄 Request Flow

How a request travels through ShareJadPi:

```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant Router
    participant Handler
    participant FileSystem
    participant Response
    
    Client->>Flask: HTTP Request
    Flask->>Flask: Parse Request
    Flask->>Router: Match Route
    Router->>Handler: Call Handler
    
    alt File Operation
        Handler->>FileSystem: Read/Write
        FileSystem-->>Handler: Result
    end
    
    Handler->>Response: Build Response
    Response-->>Flask: Response Object
    Flask-->>Client: HTTP Response
```

---

## 🧩 Core Components

### 1. Flask Application

The heart of ShareJadPi - a Flask application that handles all HTTP requests.

```python
# Application setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

**Key Features:**
- Multi-threaded request handling
- Automatic content negotiation
- Built-in development server
- Extension ecosystem

---

### 2. File Manager

Handles all file operations with safety and performance optimizations.

```mermaid
flowchart LR
    subgraph Input["📥 Input"]
        Upload["File Upload"]
        Path["File Path"]
    end
    
    subgraph FileManager["📁 File Manager"]
        Validate["Validate"]
        Secure["Secure Name"]
        Store["Store"]
        Index["Update Index"]
    end
    
    subgraph Storage["💾 Storage"]
        Disk["Local Disk"]
        Temp["Temp Files"]
    end
    
    Input --> FileManager --> Storage
    
    style FileManager fill:#065f46,stroke:#10b981,color:#fff
```

**Responsibilities:**
- Secure filename handling
- Duplicate file naming
- File type detection
- Size validation
- Directory management

---

### 3. Cloudflare Manager

Manages Cloudflare tunnel connections for internet sharing.

```python
class CloudflareManager:
    def __init__(self):
        self.process = None
        self.url = None
        self.active = False
        
    def start_tunnel(self, port=5000, file_size=0):
        """Start Cloudflare tunnel with dynamic timeout"""
        timeout = self.calculate_timeout(file_size)
        # Launch cloudflared process
        # Parse URL from output
        # Monitor for idle
        
    def stop_tunnel(self):
        """Stop the tunnel and cleanup"""
```

```mermaid
stateDiagram-v2
    [*] --> Stopped
    Stopped --> Starting: start_tunnel()
    Starting --> Running: URL received
    Starting --> Error: Failed
    Running --> Monitoring: Activity check
    Monitoring --> Running: Active
    Monitoring --> Stopping: Idle timeout
    Stopping --> Stopped: stop_tunnel()
    Error --> Stopped: Retry
```

---

### 4. Online Share Manager

Manages share tokens and access control for public links.

```mermaid
flowchart TB
    subgraph Create["📤 Create Share"]
        File["Select File"]
        Token["Generate Token"]
        URL["Build URL"]
        QR["Generate QR"]
    end
    
    subgraph Store["💾 Share Store"]
        TokenDB["Token Registry"]
        Expiry["Expiry Timer"]
        Access["Access Log"]
    end
    
    subgraph Access["📥 Access Share"]
        Validate["Validate Token"]
        Serve["Serve File"]
        Cleanup["Auto Cleanup"]
    end
    
    Create --> Store
    Store --> Access
    
    style Create fill:#065f46,stroke:#10b981,color:#fff
    style Store fill:#1e40af,stroke:#3b82f6,color:#fff
    style Access fill:#7c2d12,stroke:#f97316,color:#fff
```

---

## 🔐 Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Server
    participant TokenStore
    
    rect rgb(6, 95, 70)
        Note over User,TokenStore: Token Generation
        User->>Server: Request Share
        Server->>Server: Generate Token
        Server->>TokenStore: Store Token + Metadata
        Server-->>User: Token + URL
    end
    
    rect rgb(30, 64, 175)
        Note over User,TokenStore: Token Validation
        User->>Server: Access with Token
        Server->>TokenStore: Validate Token
        TokenStore-->>Server: Valid/Invalid
        alt Valid
            Server-->>User: Serve Content
        else Invalid
            Server-->>User: 403 Forbidden
        end
    end
    
    rect rgb(124, 45, 18)
        Note over User,TokenStore: Cleanup
        Server->>TokenStore: Check Expiry
        TokenStore-->>Server: Expired Tokens
        Server->>Server: Cleanup Resources
    end
```

### Security Measures

| Layer | Protection |
|-------|------------|
| **Network** | Local network by default |
| **Authentication** | Token-based access |
| **Files** | Secure filename sanitization |
| **Upload** | Size limits, type validation |
| **Tunnel** | Cloudflare encryption |

---

## 🌐 Network Architecture

### Local Network Mode

```mermaid
flowchart LR
    subgraph Network["🏠 Local Network (192.168.x.x)"]
        subgraph Host["Host Machine"]
            Server["ShareJadPi :5000"]
        end
        
        Desktop["💻 Desktop"]
        Laptop["💻 Laptop"]
        Phone["📱 Phone"]
        Tablet["📱 Tablet"]
    end
    
    Server <--> Desktop
    Server <--> Laptop
    Server <--> Phone
    Server <--> Tablet
    
    style Network fill:#1e40af,stroke:#3b82f6,color:#fff
    style Host fill:#065f46,stroke:#10b981,color:#fff
```

### Internet Sharing Mode

```mermaid
flowchart TB
    subgraph Local["🏠 Private Network"]
        Server["ShareJadPi"]
    end
    
    subgraph Cloudflare["☁️ Cloudflare Edge"]
        Tunnel["Encrypted Tunnel"]
        Edge["Edge Servers"]
    end
    
    subgraph Internet["🌐 Public Internet"]
        User1["User (USA)"]
        User2["User (Europe)"]
        User3["User (Asia)"]
    end
    
    Server <-->|"TLS 1.3"| Tunnel
    Tunnel <--> Edge
    Edge <--> User1
    Edge <--> User2
    Edge <--> User3
    
    style Local fill:#065f46,stroke:#10b981,color:#fff
    style Cloudflare fill:#f97316,stroke:#fb923c,color:#000
    style Internet fill:#1e40af,stroke:#3b82f6,color:#fff
```

---

## 💾 Data Flow

### Upload Flow

```mermaid
flowchart TB
    A["📁 User selects file"] --> B["🌐 Browser reads file"]
    B --> C["📤 POST /upload"]
    C --> D["⚡ Flask receives request"]
    D --> E["🔒 Secure filename"]
    E --> F["📝 Check duplicates"]
    F --> G["💾 Write to disk"]
    G --> H["📊 Update file index"]
    H --> I["✅ Return success"]
    
    style A fill:#581c87,stroke:#a855f7,color:#fff
    style D fill:#065f46,stroke:#10b981,color:#fff
    style G fill:#7c2d12,stroke:#f97316,color:#fff
    style I fill:#166534,stroke:#22c55e,color:#fff
```

### Download Flow

```mermaid
flowchart TB
    A["👆 User clicks download"] --> B["📡 GET /download/<id>"]
    B --> C["⚡ Flask routes request"]
    C --> D["🔍 Find file by ID"]
    D --> E{"File exists?"}
    E -->|Yes| F["📖 Read file"]
    E -->|No| G["❌ 404 Not Found"]
    F --> H["📤 Stream to client"]
    H --> I["✅ Download complete"]
    
    style A fill:#581c87,stroke:#a855f7,color:#fff
    style C fill:#065f46,stroke:#10b981,color:#fff
    style I fill:#166534,stroke:#22c55e,color:#fff
    style G fill:#dc2626,stroke:#ef4444,color:#fff
```

---

## ⚙️ Configuration

### Application Config

```python
# Core settings
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'ShareJadPi', 'uploads')
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
SECRET_KEY = secrets.token_hex(32)

# Server settings
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000
DEBUG = False
THREADED = True

# Cloudflare settings
TUNNEL_IDLE_TIMEOUT = 300  # 5 minutes
TUNNEL_MAX_RUNTIME = 3600  # 1 hour
```

---

## 🔄 State Management

ShareJadPi uses in-memory state for performance:

```mermaid
flowchart LR
    subgraph Memory["🧠 In-Memory State"]
        Files["File Index"]
        Shares["Active Shares"]
        Clipboard["Clipboard"]
        Settings["Settings"]
    end
    
    subgraph Disk["💾 Persistent Storage"]
        Uploads["Upload Files"]
        Config["Config File"]
    end
    
    Memory <--> Disk
    
    style Memory fill:#065f46,stroke:#10b981,color:#fff
    style Disk fill:#7c2d12,stroke:#f97316,color:#fff
```

---

## 📊 Performance Considerations

### Optimizations

| Area | Optimization |
|------|-------------|
| **File I/O** | Streaming for large files |
| **Memory** | Chunked uploads |
| **Network** | Keep-alive connections |
| **UI** | Lazy loading, virtual scrolling |
| **Cache** | In-memory file index |

### Benchmarks

```mermaid
xychart-beta
    title Upload Speed by File Size
    x-axis ["1MB", "10MB", "100MB", "500MB"]
    y-axis "Speed (MB/s)" 0 --> 100
    bar [85, 72, 58, 45]
```

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core language |
| **Framework** | Flask 3.x | HTTP routing |
| **File Handling** | Werkzeug | Secure uploads |
| **QR Codes** | qrcode + Pillow | QR generation |
| **Tunneling** | cloudflared | Internet access |
| **Build** | PyInstaller | Executable creation |
| **Installer** | Inno Setup | Windows installer |

---

## 🚀 Deployment Options

```mermaid
flowchart TB
    subgraph Development["💻 Development"]
        Python["python sharejadpi.py"]
    end
    
    subgraph Production["🏭 Production"]
        EXE["ShareJadPi.exe"]
        Installer["Windows Installer"]
    end
    
    subgraph Server["🖥️ Server"]
        Gunicorn["gunicorn"]
        Waitress["waitress"]
    end
    
    Development --> Production
    Development --> Server
    
    style Development fill:#065f46,stroke:#10b981,color:#fff
    style Production fill:#1e40af,stroke:#3b82f6,color:#fff
    style Server fill:#7c2d12,stroke:#f97316,color:#fff
```

<style>
.arch-hero {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(59,130,246,0.1));
  border-radius: 16px;
  margin-bottom: 40px;
}

.arch-hero h2 {
  margin: 0 0 12px 0;
}

.arch-hero p {
  color: var(--vp-c-text-2);
  margin: 0;
}
</style>
