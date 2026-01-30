import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  title: "ShareJadPi",
  description: "Modern Local File Sharing Application - Complete Documentation",
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#22c55e' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:title', content: 'ShareJadPi - File Sharing Made Simple' }],
  ],
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'ShareJadPi',
    
    nav: [
      { text: '🏠 Home', link: '/' },
      { text: '📖 Learn', link: '/guide/introduction' },
      { text: '🔧 Development', link: '/development/dev-server' },
      { text: '⚡ API', link: '/api' },
      { text: '🌟 GitHub', link: 'https://github.com/hetcharusat/sharejadpi' }
    ],

    sidebar: {
      '/': [
        {
          text: '👋 Start Here',
          collapsed: false,
          items: [
            { text: '1. Introduction', link: '/guide/introduction' },
            { text: '2. What is ShareJadPi?', link: '/guide/what-is-sharejadpi' },
            { text: '3. Installation', link: '/guide/installation' }
          ]
        },
        {
          text: '🎓 Learn the Basics',
          collapsed: false,
          items: [
            { text: '4. First Steps', link: '/guide/quick-start' },
            { text: '5. Uploading Files', link: '/guide/uploading' },
            { text: '6. Downloading Files', link: '/guide/downloading' },
            { text: '7. Managing Files', link: '/guide/managing-files' }
          ]
        },
        {
          text: '🏗️ Understanding ShareJadPi',
          collapsed: false,
          items: [
            { text: '8. How It Works', link: '/architecture' },
            { text: '9. Features Breakdown', link: '/features' },
            { text: '10. Development Timeline', link: '/timeline' }
          ]
        },
        {
          text: '💻 For Developers',
          collapsed: false,
          items: [
            { text: '11. API Reference', link: '/api' },
            { text: '12. Development Server', link: '/development/dev-server' },
            { text: '13. Configuration Options', link: '/guide/configuration' },
            { text: '14. Contributing', link: '/development/contributing' }
          ]
        },
        {
          text: '🚀 Advanced',
          collapsed: false,
          items: [
            { text: '15. Deployment Guide', link: '/DEPLOYMENT' },
            { text: '16. Future Roadmap', link: '/guide/roadmap' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/hetcharusat/sharejadpi' }
    ],

    footer: {
      message: 'Built with ❤️ by Het Charusat',
      copyright: 'ShareJadPi - Modern File Sharing Application'
    },
    
    search: {
      provider: 'local'
    },
    
    editLink: {
      pattern: 'https://github.com/hetcharusat/sharejadpi/edit/main/SGP_phase1/docs/:path',
      text: 'Edit this page on GitHub'
    }
  },
  
  mermaid: {
    theme: 'dark'
  }
}))
