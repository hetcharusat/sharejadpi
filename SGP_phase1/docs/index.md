---
layout: home

hero:
  name: "ShareJadPi"
  text: "Modern File Sharing Application"
  tagline: "Share files effortlessly on your local network"
  image: /icon.png
  actions:
    - theme: brand
      text: Get Started
      link: /guide/introduction
    - theme: alt
      text: View on GitHub
      link: https://github.com/hetcharusat/sharejadpi

features:
  - icon: 📂
    title: Web File Sharing
    details: Seamlessly share files across your local network through an intuitive web interface.
    linkText: "Status: ✅ Implemented"
  
  - icon: 🎨
    title: Modern Dark UI
    details: Beautiful, responsive interface with smooth animations and modern design patterns.
    linkText: "Status: ✅ Implemented"
  
  - icon: 🌐
    title: Local Network Ready
    details: Instantly accessible on your local network - no complex configuration needed.
    linkText: "Status: ✅ Implemented"

  - icon: 🔐
    title: Token Security System
    details: Secure authentication system with token-based access control (Phase 3 feature).
    linkText: "Status: 📅 Planned"

  - icon: 🖱️
    title: Context Menu Integration
    details: Right-click any file to instantly share it via ShareJadPi (Phase 3 feature).
    linkText: "Status: 📅 Planned"

  - icon: 📱
    title: QR Code Sharing
    details: Generate QR codes for quick mobile device access (Phase 4 feature).
    linkText: "Status: 📅 Planned"
---

## Development Status

<div class="status-card">

### 🚀 Phase 2 - Core Development In Progress (45%)

ShareJadPi is actively being developed with major infrastructure improvements and feature additions.

<div class="progress-container">
  <div class="progress-bar">
    <div class="progress-fill phase1" style="width: 100%">Phase 1: 100%</div>
  </div>
  <div class="progress-bar">
    <div class="progress-fill phase2" style="width: 45%">Phase 2: 45%</div>
  </div>
  <div class="progress-bar">
    <div class="progress-fill phase3" style="width: 0%">Phase 3: 0%</div>
  </div>
  <div class="progress-bar">
    <div class="progress-fill phase4" style="width: 0%">Phase 4: 0%</div>
  </div>
  <div class="progress-bar">
    <div class="progress-fill phase5" style="width: 0%">Phase 5: 0%</div>
  </div>
</div>

</div>

<style>
.status-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 24px;
  margin: 24px 0;
}

.progress-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

.progress-bar {
  height: 32px;
  background: var(--vp-c-bg-mute);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  transition: width 0.3s ease;
  color: white;
}

.progress-fill.phase1 {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.progress-fill.phase2 {
  background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
}

.progress-fill.phase3 {
  background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%);
}

.progress-fill.phase4 {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.progress-fill.phase5 {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}
</style>

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hetcharusat/sharejadpi.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python sharejadpi.py
```

## What's Next?

- 🔄 Performance optimization and code refactoring
- 🛡️ Enhanced error handling and validation
- 🧪 Comprehensive testing framework
- 📖 API documentation improvements
- 🔐 Token authentication system (Phase 3)
