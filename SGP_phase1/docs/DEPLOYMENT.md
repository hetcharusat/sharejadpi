# VitePress Build Configuration

## Build Settings for Vercel

### Framework Preset
- **Framework:** VitePress
- **Node Version:** 20.x

### Build Configuration
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".vitepress/dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

### Environment Variables (if needed)
```bash
NODE_VERSION=20.x
```

### Root Directory
Set to: `docs` (or wherever your VitePress documentation lives)

## Vercel Deployment Steps

### 1. Connect GitHub Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository: `hetcharusat/sharejadpi`

### 2. Configure Project Settings
```yaml
Framework Preset: VitePress
Root Directory: SGP_phase1/docs
Build Command: npm run build
Output Directory: .vitepress/dist
Install Command: npm install
Node.js Version: 20.x
```

### 3. Deploy
- Click "Deploy"
- Vercel will automatically build and deploy your documentation
- You'll get a URL like: `https://sharejadpi.vercel.app`

## Manual Vercel CLI Deployment

### Install Vercel CLI
```bash
npm i -g vercel
```

### Login to Vercel
```bash
vercel login
```

### Deploy from docs directory
```bash
cd docs
vercel --prod
```

### Configuration Questions
```
? Set up and deploy "~/sharejadpi/SGP_phase1/docs"? [Y/n] Y
? Which scope? Your Name
? Link to existing project? [y/N] N
? What's your project's name? sharejadpi-docs
? In which directory is your code located? ./
? Want to modify these settings? [y/N] N
```

## Automatic Deployment

### GitHub Integration
Vercel will automatically deploy when you push to:
- **Production Branch:** `main` → https://sharejadpi.vercel.app
- **Preview Branches:** Any other branch → https://sharejadpi-{branch}.vercel.app

### Build Process
```mermaid
graph LR
    A[Git Push] --> B[Vercel Webhook]
    B --> C[Clone Repository]
    C --> D[Install Dependencies]
    D --> E[Run Build Command]
    E --> F[Generate Static Files]
    F --> G[Deploy to CDN]
    G --> H[Live URL]
    
    style A fill:#3b82f6
    style E fill:#10b981
    style H fill:#8b5cf6
```

## Build Commands Reference

### Development Server
```bash
npm run dev
# Starts VitePress dev server at http://localhost:5173
```

### Production Build
```bash
npm run build
# Builds static files to .vitepress/dist
```

### Preview Build
```bash
npm run preview
# Preview production build locally
```

## Troubleshooting

### Build Fails with "command not found"
**Solution:** Make sure `package.json` has correct scripts:
```json
{
  "scripts": {
    "build": "vitepress build"
  }
}
```

### "Cannot find module 'vitepress'"
**Solution:** Ensure dependencies are in `package.json`:
```json
{
  "dependencies": {
    "vitepress": "^1.6.4"
  }
}
```

### Mermaid diagrams not rendering
**Solution:** Install Mermaid plugin:
```bash
npm install vitepress-plugin-mermaid mermaid
```

And configure in `.vitepress/config.mjs`:
```javascript
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid({
  // your config
})
```

### Build succeeds but site is blank
**Solution:** Check output directory is set to `.vitepress/dist`

### 404 on nested routes
**Solution:** Ensure `vercel.json` has proper rewrites:
```json
{
  "rewrites": [
    { "source": "/:path*", "destination": "/:path*" }
  ]
}
```

## Vercel Project Settings

### General Settings
- **Project Name:** sharejadpi-docs
- **Framework:** VitePress
- **Root Directory:** `SGP_phase1/docs` (if deploying from subdirectory)
- **Build & Output Settings:**
  - Build Command: `npm run build`
  - Output Directory: `.vitepress/dist`
  - Install Command: `npm install`

### Environment Variables (Optional)
```
NODE_VERSION=20.x
VITE_BASE_URL=/
```

### Git Integration
- **Production Branch:** main
- **Deploy Hooks:** Enabled
- **Ignored Build Step:** Use `.vercelignore` to skip builds when no docs changes

## Performance Optimization

### Edge Network
Vercel automatically deploys to:
- Global CDN with 100+ edge locations
- Automatic SSL/TLS certificates
- HTTP/2 & HTTP/3 support
- Smart CDN caching

### Build Cache
- Node modules cached between builds
- Faster subsequent deployments
- Incremental static regeneration

### Analytics
Enable Vercel Analytics:
```bash
npm install @vercel/analytics
```

Add to `.vitepress/theme/index.js`:
```javascript
import { inject } from '@vercel/analytics'
inject()
```

## Custom Domain (Optional)

### Add Custom Domain
1. Go to Project Settings → Domains
2. Add your domain: `docs.sharejadpi.com`
3. Configure DNS records:
   ```
   Type: CNAME
   Name: docs
   Value: cname.vercel-dns.com
   ```

### SSL Certificate
- Automatically provisioned
- Auto-renewal
- Free with Vercel

## Deployment Status Badge

Add to README:
```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/hetcharusat/sharejadpi)
```

## Local Testing Before Deploy

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

Visit: http://localhost:4173

## Deployment Checklist

- [x] `package.json` with correct scripts
- [x] `vercel.json` configuration
- [x] `.vitepress/config.mjs` configured
- [x] All markdown files created
- [x] Mermaid plugin installed
- [x] GitHub repository connected
- [ ] Push to main branch
- [ ] Vercel auto-deploys
- [ ] Check live URL
- [ ] Test all pages and diagrams
- [ ] Configure custom domain (optional)

## Support

- **Vercel Docs:** https://vercel.com/docs
- **VitePress Docs:** https://vitepress.dev
- **GitHub Issues:** https://github.com/hetcharusat/sharejadpi/issues
