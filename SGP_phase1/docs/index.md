---
layout: home

hero:
  name: "ShareJadPi"
  text: "Local File Sharing Made Simple"
  tagline: "A modern, elegant solution for sharing files across your local network. No cloud, no accounts, just seamless file transfer."
  actions:
    - theme: brand
      text: Get Started →
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/hetcharusat/sharejadpi

features:
  - icon: 📂
    title: Drag & Drop Upload
    details: Simply drag files into the browser or click to select. Multiple file uploads with real-time progress tracking.
  
  - icon: 🎨
    title: Modern Dark UI
    details: Beautiful, responsive interface with smooth animations, gradient accents, and a sleek dark theme that's easy on the eyes.
  
  - icon: 🌐
    title: Zero Configuration
    details: Start the server and access from any device on your network. Auto-detects IP and opens in browser automatically.

  - icon: ⚡
    title: Fast & Lightweight
    details: Built with Flask for speed. Minimal dependencies, low resource usage, and instant file transfers.

  - icon: 🔒
    title: Local & Private
    details: Files stay on your network. No cloud uploads, no external servers, complete privacy for your data.

  - icon: 📱
    title: Cross-Platform
    details: Access from Windows, Mac, Linux, iOS, or Android. Any device with a web browser works perfectly.
---

<div class="vp-doc" style="padding: 2rem;">

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/hetcharusat/sharejadpi.git
cd sharejadpi

# Install dependencies
pip install -r requirements.txt

# Run ShareJadPi
python sharejadpi.py
```

Your browser will automatically open to the ShareJadPi interface!

## 📊 System Architecture

The following diagram shows how ShareJadPi works:

```mermaid
flowchart TB
    subgraph Client["🌐 Client Devices"]
        Browser["Web Browser"]
        Mobile["Mobile Device"]
    end
    
    subgraph Server["⚡ ShareJadPi Server"]
        Flask["Flask App"]
        Routes["API Routes"]
        FileManager["File Manager"]
    end
    
    subgraph Storage["💾 Storage"]
        UploadDir["Upload Directory"]
        TempFiles["Temporary Files"]
    end
    
    Browser -->|HTTP Request| Flask
    Mobile -->|HTTP Request| Flask
    Flask --> Routes
    Routes --> FileManager
    FileManager --> UploadDir
    FileManager --> TempFiles
    
    style Client fill:#1e293b,stroke:#3b82f6,color:#fff
    style Server fill:#1e293b,stroke:#22c55e,color:#fff
    style Storage fill:#1e293b,stroke:#f59e0b,color:#fff
```

## 💡 Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **File Upload** | Drag-drop or click-to-upload with progress | ✅ Available |
| **File Download** | Direct download links for all files | ✅ Available |
| **File Management** | Delete files through the web interface | ✅ Available |
| **Auto IP Detection** | Automatically finds your network IP | ✅ Available |
| **Dark Theme** | Modern dark UI with gradient accents | ✅ Available |
| **Mobile Responsive** | Works on all screen sizes | ✅ Available |

## 🛠️ Development Server

For local development and testing, use the lightweight dev server:

```bash
cd SGP_phase1
python sharejadpi-dev.py
```

The dev server includes:
- 🔄 Hot reload for instant feedback
- 📊 Debug mode with detailed logging  
- 🎯 Simplified codebase for easy modification

[Learn more about development →](/development/dev-server)

## 📈 Project Status

<div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(59,130,246,0.1)); border-radius: 12px; padding: 20px; border: 1px solid rgba(34,197,94,0.3); margin: 20px 0;">

**Current Version:** `4.5.4`

| Milestone | Progress | Status |
|-----------|----------|--------|
| Core File Sharing | 100% | ✅ Complete |
| Modern UI Design | 100% | ✅ Complete |
| Development Tools | 100% | ✅ Complete |
| Documentation | 90% | 🔄 In Progress |
| Testing Suite | 50% | 🔄 In Progress |

</div>

## 🤝 Contributing

We welcome contributions! Check out our [Contributing Guide](/development/contributing) to get started.

</div>
