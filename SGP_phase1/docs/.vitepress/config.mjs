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
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Development', link: '/development/dev-server' },
      { text: 'API', link: '/api' },
      { text: 'GitHub', link: 'https://github.com/hetcharusat/sharejadpi' }
    ],

    sidebar: {
      '/': [
        {
          text: '📚 Introduction',
          items: [
            { text: 'Overview', link: '/' },
            { text: 'Features', link: '/features' },
            { text: 'Timeline', link: '/timeline' }
          ]
        },
        {
          text: '🚀 Getting Started',
          items: [
            { text: 'Installation', link: '/guide/getting-started' },
            { text: 'Quick Start', link: '/guide/quick-start' },
            { text: 'Configuration', link: '/guide/configuration' }
          ]
        },
        {
          text: '💻 Development',
          items: [
            { text: 'Dev Server', link: '/development/dev-server' },
            { text: 'Architecture', link: '/architecture' },
            { text: 'Contributing', link: '/development/contributing' }
          ]
        },
        {
          text: '📖 Reference',
          items: [
            { text: 'API Documentation', link: '/api' },
            { text: 'Deployment', link: '/DEPLOYMENT' }
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
