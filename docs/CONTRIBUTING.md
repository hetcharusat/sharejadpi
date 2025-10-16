# Contributing to ShareJadPi

Thank you for your interest in contributing! 🎉

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Getting Started

1. **Fork and clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/sharejadpi.git
cd sharejadpi
```

2. **Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
python sharejadpi.py
```

---

## 📦 Building

### Build Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build from the build_tools directory
cd build_tools
pyinstaller --clean ShareJadPi-4.0.0.spec

# Output: ../dist/ShareJadPi-4.0.0.exe
```

### Build Installer (Requires Inno Setup)

1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php)
2. Open `build_tools/ShareJadPi-Installer-4.0.0.iss` in Inno Setup
3. Click "Compile"
4. Output: `installer_output\ShareJadPi-4.0.0-Setup.exe`

---

## 🤝 How to Contribute

### Reporting Bugs
- Use [GitHub Issues](https://github.com/hetcharusat/sharejadpi/issues)
- Include steps to reproduce
- Mention your OS version and Python version

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and use case
- Explain why it would be useful

### Submitting Pull Requests

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Follow existing code style
   - Test thoroughly
   - Update documentation if needed

3. **Commit your changes**
```bash
git commit -m "Add: brief description of your changes"
```

4. **Push and create PR**
```bash
git push origin feature/your-feature-name
```

---

## 📁 Project Structure

```
sharejadpi/
├── sharejadpi.py              # Main application
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
├── README.md                  # Main documentation
├── templates/                 # HTML templates
│   └── index.html            # Web interface
├── static/                    # Static assets
├── assets/                    # Project assets
│   ├── icon.ico              # App icon
│   ├── icon.png              # PNG icon
│   └── vidss/                # Demo screenshots/videos
├── build_tools/               # Build configuration
│   ├── ShareJadPi-4.0.0.spec         # PyInstaller config
│   ├── ShareJadPi-Installer-4.0.0.iss # Inno Setup config
│   └── create_icon.py         # Icon generator
└── docs/                      # Documentation
    └── CONTRIBUTING.md        # This file
```

---

## 🎨 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

---

## 🧪 Testing

Before submitting:
1. Test the app runs without errors
2. Test on different Windows versions if possible
3. Test firewall configuration works
4. Test file upload/download functionality
5. Test on mobile devices

---

## 📝 Commit Message Guidelines

- **Add:** New feature
- **Fix:** Bug fix
- **Update:** Modify existing feature
- **Remove:** Delete feature/code
- **Docs:** Documentation changes
- **Build:** Build system changes

Example: `Add: network speed test feature`

---

## 🚀 Release Process (Maintainers)

1. Update version in `sharejadpi.py`
2. Update version in `.spec` and `.iss` files
3. Build executable and installer
4. Test thoroughly
5. Create GitHub release with binaries
6. Update README download link

---

## 💬 Questions?

- Open a [Discussion](https://github.com/hetcharusat/sharejadpi/discussions)
- Check existing issues for answers

---

Thank you for contributing! ❤️
