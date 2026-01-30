import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "ShareJadPi Docs",
  description: "Modern File Sharing Application - Development Documentation",
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Timeline', link: '/timeline' },
      { text: 'GitHub', link: 'https://github.com/hetcharusat/sharejadpi' }
    ],

    sidebar: [
      {
        text: 'Documentation',
        items: [
          { text: 'Introduction', link: '/' },
          { text: 'Development Timeline', link: '/timeline' },
          { text: 'System Architecture', link: '/architecture' },
          { text: 'Features', link: '/features' },
          { text: 'API Documentation', link: '/api' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/hetcharusat/sharejadpi' }
    ],

    footer: {
      message: 'ShareJadPi - Modern File Sharing Application'
    }
  }
})
