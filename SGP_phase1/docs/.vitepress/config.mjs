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
          text: '🏗️ Architecture & Design',
          collapsed: true,
          items: [
            { text: '8. System Architecture', link: '/architecture' },
            { text: '9. Design Patterns', link: '/architecture#design-patterns' },
            { text: '10. Data Flow', link: '/architecture#data-flow-diagrams' },
            { text: '11. Security Model', link: '/architecture#security-architecture' }
          ]
        },
        {
          text: '✨ Features & Timeline',
          collapsed: true,
          items: [
            { text: '12. Features Breakdown', link: '/features' },
            { text: '13. Development Timeline', link: '/timeline' },
            { text: '14. Future Roadmap', link: '/guide/roadmap' }
          ]
        },
        {
          text: '💻 For Developers',
          collapsed: true,
          items: [
            { text: '15. API Reference', link: '/api' },
            { text: '16. Development Server', link: '/development/dev-server' },
            { text: '17. Configuration', link: '/guide/configuration' },
            { text: '18. Contributing', link: '/development/contributing' }
          ]
        },
        {
          text: '🚀 Deployment',
          collapsed: true,
          items: [
            { text: '19. Deployment Guide', link: '/DEPLOYMENT' }
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
