# 👋 Welcome to ShareJadPi

<div class="intro-hero">
  <h2>Your Journey Starts Here</h2>
  <p>Welcome! This documentation will guide you from zero to expert, step by step.</p>
</div>

## 🎯 What You'll Learn

This documentation follows a clear learning path:

```mermaid
graph LR
    A[👋 Start Here] --> B[🎓 Learn Basics]
    B --> C[🏗️ Understanding]
    C --> D[💻 Development]
    D --> E[🚀 Advanced]
    
    style A fill:#10b981,stroke:#059669,color:#fff
    style B fill:#3b82f6,stroke:#2563eb,color:#fff
    style C fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style D fill:#f59e0b,stroke:#d97706,color:#fff
    style E fill:#ef4444,stroke:#dc2626,color:#fff
```

### 📚 Learning Path

<div class="learning-path">

**Phase 1: Start Here** ⭐ *You are here!*
1. **Introduction** (this page) - Overview and learning path
2. **What is ShareJadPi?** - Core concept and purpose
3. **Installation** - Get ShareJadPi running on your machine

**Phase 2: Learn the Basics** 🎓
4. **First Steps** - Launch and access the app
5. **Uploading Files** - Learn to upload files
6. **Downloading Files** - Learn to download files
7. **Managing Files** - Delete and organize files

**Phase 3: Understanding ShareJadPi** 🏗️
8. **How It Works** - Architecture and technical design
9. **Features Breakdown** - Deep dive into all features
10. **Development Timeline** - Project evolution and history

**Phase 4: For Developers** 💻
11. **API Reference** - Complete REST API documentation
12. **Development Server** - Development environment setup
13. **Configuration Options** - Customize ShareJadPi
14. **Contributing** - Help improve ShareJadPi

**Phase 5: Advanced** 🚀
15. **Deployment Guide** - Deploy for production
16. **Future Roadmap** - What's coming next

</div>

---

## 🎓 Who Is This For?

<div class="audience-grid">

<div class="audience-card">
  <div class="audience-icon">👤</div>
  <h3>End Users</h3>
  <p>Want to share files on your local network</p>
  <ul>
    <li>✅ Start with Phases 1-2</li>
    <li>✅ Learn basic operations</li>
    <li>✅ Skip technical details</li>
  </ul>
</div>

<div class="audience-card">
  <div class="audience-icon">💻</div>
  <h3>Developers</h3>
  <p>Want to integrate or extend ShareJadPi</p>
  <ul>
    <li>✅ Read all phases</li>
    <li>✅ Focus on Phases 3-4</li>
    <li>✅ Use API reference</li>
  </ul>
</div>

<div class="audience-card">
  <div class="audience-icon">🏢</div>
  <h3>Organizations</h3>
  <p>Want to deploy for teams</p>
  <ul>
    <li>✅ Read Phases 1, 3, 5</li>
    <li>✅ Review security notes</li>
    <li>✅ Check deployment guide</li>
  </ul>
</div>

</div>

---

## ⚡ Quick Navigation

<div class="quick-nav">

**If you want to...**

- 🚀 **Get started immediately** → [Installation →](/guide/installation)
- 📖 **Understand what ShareJadPi is** → [What is ShareJadPi? →](/guide/what-is-sharejadpi)
- 💻 **Use the API** → [API Reference →](/api)
- 🔧 **Contribute to development** → [Contributing →](/development/contributing)
- 🏗️ **Understand the architecture** → [Architecture →](/architecture)

</div>

---

## 📖 How to Use This Documentation

### 🎯 Recommended Path

<div class="callout tip">
<strong>💡 First Time Here?</strong>

Follow the numbered sequence in the sidebar (1 → 16). Each page builds on the previous one.
</div>

### 🔍 Search Anything

Use the search bar at the top to find specific topics quickly.

### 🌐 Navigation Tips

- **Sidebar numbers** show the recommended reading order
- **Collapsed sections** can be expanded by clicking
- **"Edit on GitHub"** link at the bottom of each page for corrections
- **Previous/Next** buttons at the bottom navigate sequentially

---

## 🎯 What is ShareJadPi?

<div class="preview-card">

**ShareJadPi** is a modern, lightweight file sharing application for local networks.

Think of it as your personal file sharing server that runs on your computer. Anyone on your network can:
- Upload files through a web browser
- Download files you've shared
- All without installing anything!

**Current Version:** 4.5.4-dev (Development)

</div>

### Key Highlights

<div class="highlight-grid">

<div class="highlight-item">
  <span class="highlight-number">813</span>
  <span class="highlight-label">Lines of Code</span>
</div>

<div class="highlight-item">
  <span class="highlight-number">6</span>
  <span class="highlight-label">API Endpoints</span>
</div>

<div class="highlight-item">
  <span class="highlight-number">100%</span>
  <span class="highlight-label">Open Source</span>
</div>

<div class="highlight-item">
  <span class="highlight-number">5</span>
  <span class="highlight-label">Minutes to Setup</span>
</div>

</div>

---

## 🚀 Ready to Start?

<div class="cta-section">

### Next Step: Learn What ShareJadPi Is

Understanding the core concept will help you get the most out of ShareJadPi.

[Continue to "What is ShareJadPi?" →](/guide/what-is-sharejadpi){.cta-button}

</div>

---

## 💬 Need Help?

<div class="help-section">

**Found an issue or have questions?**

- 🐛 Report bugs on [GitHub Issues](https://github.com/hetcharusat/sharejadpi/issues)
- 💡 Suggest features in [Discussions](https://github.com/hetcharusat/sharejadpi/discussions)
- 📧 Contact: [Your Email]
- ⭐ Star the project if you find it useful!

</div>

---

<style>
.intro-hero {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
  border-radius: 16px;
  margin-bottom: 3rem;
}

.intro-hero h2 {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
}

.learning-path {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
}

.learning-path h4 {
  color: #10b981;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.audience-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.audience-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.audience-card:hover {
  transform: translateY(-4px);
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
}

.audience-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.audience-card h3 {
  color: #10b981;
  margin-bottom: 0.5rem;
}

.audience-card ul {
  text-align: left;
  margin-top: 1rem;
}

.quick-nav {
  background: rgba(59, 130, 246, 0.1);
  border-left: 4px solid #3b82f6;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.quick-nav ul {
  margin: 1rem 0;
}

.callout {
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid;
  margin: 2rem 0;
}

.callout.tip {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
}

.preview-card {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
}

.highlight-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.highlight-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
}

.highlight-number {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #059669);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.highlight-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 0.5rem;
}

.cta-section {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
  border-radius: 16px;
  margin: 3rem 0;
}

.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white !important;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.help-section {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
}
</style>
