# System Architecture

## Overview

ShareJadPi follows a modern client-server architecture with Flask backend and responsive web frontend.

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser] --> B[HTML/CSS/JS Frontend]
        B --> C[File Upload Interface]
        B --> D[File Browser]
        B --> E[Settings Panel]
    end
    
    subgraph "Network Layer"
        F[HTTP/HTTPS Protocol]
        G[Local Network]
        H[Port 5000]
    end
    
    subgraph "Server Layer"
        I[Flask Application]
        I --> J[Route Handlers]
        I --> K[Template Engine]
        I --> L[Static File Server]
    end
    
    subgraph "Business Logic"
        M[File Manager]
        N[Network Manager]
        O[Security Handler]
        P[Error Handler]
    end
    
    subgraph "Storage Layer"
        Q[(File System)]
        R[(Temp Storage)]
        S[(Configuration)]
    end
    
    B --> F
    F --> I
    J --> M
    J --> N
    J --> O
    M --> Q
    M --> R
    N --> S
    O --> S
    
    style A fill:#3b82f6
    style I fill:#10b981
    style Q fill:#f59e0b
    style M fill:#8b5cf6
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        A1[Upload Component]
        A2[File List Component]
        A3[Progress Bar Component]
        A4[Notification Component]
        A5[Theme Manager]
    end
    
    subgraph "Backend Modules"
        B1[app.py - Main Server]
        B2[file_handler.py]
        B3[network_utils.py]
        B4[config_manager.py]
    end
    
    subgraph "Core Services"
        C1[File Upload Service]
        C2[File Download Service]
        C3[Network Discovery]
        C4[Error Logging]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> C1
    B1 --> C2
    B1 --> C3
    B1 --> C4
    
    B2 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    
    style B1 fill:#10b981
    style C1 fill:#3b82f6
    style C2 fill:#3b82f6
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant FileSystem
    participant Network
    
    User->>Browser: Open ShareJadPi
    Browser->>Flask: GET /
    Flask->>Browser: Return index.html
    
    User->>Browser: Select File
    Browser->>Browser: Validate File
    
    Browser->>Flask: POST /upload
    Flask->>Flask: Validate Request
    Flask->>FileSystem: Save File
    FileSystem-->>Flask: Confirm Save
    Flask-->>Browser: Success Response
    Browser-->>User: Show Success Notification
    
    User->>Browser: Request File List
    Browser->>Flask: GET /files
    Flask->>FileSystem: Read Directory
    FileSystem-->>Flask: File List
    Flask-->>Browser: JSON Response
    Browser-->>User: Display Files
    
    User->>Browser: Download File
    Browser->>Flask: GET /download/filename
    Flask->>FileSystem: Read File
    FileSystem-->>Flask: File Stream
    Flask-->>Browser: File Response
    Browser-->>User: Download Complete
```

## Network Architecture

```mermaid
graph TB
    subgraph "Local Network 192.168.x.x"
        subgraph "Server Machine"
            A[ShareJadPi Server]
            A --> B[Flask :5000]
            B --> C[Network Interface]
        end
        
        subgraph "Client Devices"
            D1[Desktop PC]
            D2[Laptop]
            D3[Mobile Device]
            D4[Tablet]
        end
        
        C <--> E[Router/Switch]
        E <--> D1
        E <--> D2
        E <--> D3
        E <--> D4
    end
    
    subgraph "External Access - Phase 3"
        F[Cloudflare Tunnel]
        G[Public Internet]
        F -.-> C
        G -.-> F
    end
    
    style A fill:#10b981
    style E fill:#3b82f6
    style F fill:#f59e0b
```

## Security Architecture (Phase 3)

```mermaid
graph TB
    subgraph "Authentication Layer"
        A[Token Generator]
        B[Token Validator]
        C[Session Manager]
    end
    
    subgraph "Authorization Layer"
        D[Access Control]
        E[Permission Manager]
        F[Role Manager]
    end
    
    subgraph "Encryption Layer"
        G[HTTPS/TLS]
        H[File Encryption]
        I[Password Hashing]
    end
    
    subgraph "Security Monitoring"
        J[Access Logger]
        K[Intrusion Detection]
        L[Rate Limiter]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    
    G --> H
    H --> I
    
    J --> K
    K --> L
    
    style A fill:#ef4444
    style G fill:#10b981
    style J fill:#f59e0b
```

## Database Schema (Phase 3)

```mermaid
erDiagram
    USERS ||--o{ FILES : uploads
    USERS ||--o{ TOKENS : generates
    USERS ||--o{ SESSIONS : creates
    FILES ||--o{ DOWNLOADS : tracked_by
    
    USERS {
        int id PK
        string username
        string password_hash
        string email
        datetime created_at
        boolean is_active
    }
    
    FILES {
        int id PK
        string filename
        string filepath
        int size
        string mime_type
        int uploader_id FK
        datetime uploaded_at
        int download_count
    }
    
    TOKENS {
        int id PK
        string token_value
        int user_id FK
        datetime created_at
        datetime expires_at
        boolean is_active
    }
    
    SESSIONS {
        int id PK
        string session_id
        int user_id FK
        string ip_address
        datetime created_at
        datetime last_activity
    }
    
    DOWNLOADS {
        int id PK
        int file_id FK
        int user_id FK
        string ip_address
        datetime downloaded_at
    }
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A[Python 3.x]
        B[Flask Dev Server]
        C[Local Testing]
    end
    
    subgraph "Build Process"
        D[PyInstaller]
        E[Asset Bundling]
        F[Icon Generation]
    end
    
    subgraph "Distribution"
        G[Standalone EXE]
        H[Installer Package]
        I[GitHub Release]
    end
    
    subgraph "Production Deployment"
        J[Windows Machine]
        K[Auto-Start Service]
        L[Firewall Configuration]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    
    style D fill:#10b981
    style G fill:#3b82f6
    style J fill:#f59e0b
```

## Technology Stack

```mermaid
mindmap
  root((ShareJadPi))
    Backend
      Python 3.x
      Flask 3.x
      Werkzeug
      Jinja2
    Frontend
      HTML5
      CSS3
        Animations
        Grid/Flexbox
        Dark Theme
      JavaScript
        ES6+
        Fetch API
        DOM Manipulation
    Packaging
      PyInstaller
      InnoSetup
      Auto-py-to-exe
    Development
      VS Code
      Git
      GitHub
      VitePress
    Testing
      Pytest
      Unit Tests
      Integration Tests
    Future
      Socket.IO
      SQLite
      Redis
      Docker
```

## Module Dependency Graph

```mermaid
graph LR
    A[sharejadpi.py] --> B[Flask]
    A --> C[werkzeug]
    A --> D[os/sys]
    A --> E[socket]
    
    B --> F[render_template]
    B --> G[request]
    B --> H[send_file]
    B --> I[jsonify]
    
    C --> J[secure_filename]
    C --> K[FileStorage]
    
    E --> L[gethostname]
    E --> M[gethostbyname]
    
    style A fill:#10b981
    style B fill:#3b82f6
    style C fill:#8b5cf6
    style E fill:#f59e0b
```

## Performance Optimization Strategy

```mermaid
graph TB
    subgraph "Frontend Optimization"
        A1[Code Minification]
        A2[Image Optimization]
        A3[Lazy Loading]
        A4[Browser Caching]
    end
    
    subgraph "Backend Optimization"
        B1[File Streaming]
        B2[Memory Management]
        B3[Connection Pooling]
        B4[Response Compression]
    end
    
    subgraph "Network Optimization"
        C1[HTTP/2 Support]
        C2[Keep-Alive]
        C3[CDN Integration]
        C4[Load Balancing]
    end
    
    subgraph "Database Optimization"
        D1[Query Optimization]
        D2[Indexing]
        D3[Caching Layer]
        D4[Connection Pooling]
    end
    
    A1 --> E[Faster Page Load]
    A2 --> E
    B1 --> F[Reduced Memory Usage]
    B2 --> F
    C1 --> G[Lower Latency]
    C2 --> G
    D1 --> H[Faster Queries]
    D2 --> H
    
    style E fill:#10b981
    style F fill:#3b82f6
    style G fill:#8b5cf6
    style H fill:#f59e0b
```

::: tip Interactive Diagrams
All diagrams above are rendered with Mermaid and support interactive features when viewed in the documentation.
:::
