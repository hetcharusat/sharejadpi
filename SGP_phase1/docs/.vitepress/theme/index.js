import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router, siteData }) {
    // Register after mounted hook for Mermaid interactivity
    if (typeof window !== 'undefined') {
      // Wait for page to load, then add interactivity
      router.onAfterRouteChanged = () => {
        setTimeout(() => {
          initMermaidInteractivity()
        }, 500)
      }
      
      // Initial load
      setTimeout(() => {
        initMermaidInteractivity()
      }, 1000)
    }
  }
}

function initMermaidInteractivity() {
  const mermaidContainers = document.querySelectorAll('.mermaid')
  
  mermaidContainers.forEach(container => {
    // Skip if already processed
    if (container.classList.contains('mermaid-interactive')) return
    container.classList.add('mermaid-interactive')
    
    // Create wrapper if not exists
    let wrapper = container.parentElement
    if (!wrapper.classList.contains('mermaid-wrapper')) {
      wrapper = document.createElement('div')
      wrapper.className = 'mermaid-wrapper'
      container.parentNode.insertBefore(wrapper, container)
      wrapper.appendChild(container)
    }
    
    // Add controls
    const controls = document.createElement('div')
    controls.className = 'mermaid-controls'
    controls.innerHTML = `
      <button class="mermaid-btn zoom-in" title="Zoom In">🔍+</button>
      <button class="mermaid-btn zoom-out" title="Zoom Out">🔍−</button>
      <button class="mermaid-btn reset" title="Reset">↺</button>
      <button class="mermaid-btn fullscreen" title="Fullscreen">⛶</button>
    `
    wrapper.insertBefore(controls, container)
    
    // State
    let scale = 1
    let posX = 0
    let posY = 0
    let isDragging = false
    let startX = 0
    let startY = 0
    
    const svg = container.querySelector('svg') || container
    
    // Zoom In
    controls.querySelector('.zoom-in').addEventListener('click', () => {
      scale = Math.min(scale + 0.25, 4)
      updateTransform()
    })
    
    // Zoom Out
    controls.querySelector('.zoom-out').addEventListener('click', () => {
      scale = Math.max(scale - 0.25, 0.25)
      updateTransform()
    })
    
    // Reset
    controls.querySelector('.reset').addEventListener('click', () => {
      scale = 1
      posX = 0
      posY = 0
      updateTransform()
    })
    
    // Fullscreen
    controls.querySelector('.fullscreen').addEventListener('click', () => {
      wrapper.classList.toggle('mermaid-fullscreen')
      const btn = controls.querySelector('.fullscreen')
      btn.textContent = wrapper.classList.contains('mermaid-fullscreen') ? '✕' : '⛶'
      
      // Reset transform when entering fullscreen
      if (wrapper.classList.contains('mermaid-fullscreen')) {
        scale = 1
        posX = 0
        posY = 0
        updateTransform()
      }
    })
    
    // Scroll wheel zoom
    wrapper.addEventListener('wheel', (e) => {
      e.preventDefault()
      const delta = e.deltaY > 0 ? -0.15 : 0.15
      const newScale = Math.max(0.25, Math.min(4, scale + delta))
      
      // Zoom toward mouse pointer
      const rect = wrapper.getBoundingClientRect()
      const mouseX = e.clientX - rect.left
      const mouseY = e.clientY - rect.top
      
      const scaleRatio = newScale / scale
      posX = mouseX - (mouseX - posX) * scaleRatio
      posY = mouseY - (mouseY - posY) * scaleRatio
      
      scale = newScale
      updateTransform()
    }, { passive: false })
    
    // Pan with mouse drag
    container.addEventListener('mousedown', (e) => {
      isDragging = true
      startX = e.clientX - posX
      startY = e.clientY - posY
      container.style.cursor = 'grabbing'
      e.preventDefault()
    })
    
    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return
      posX = e.clientX - startX
      posY = e.clientY - startY
      updateTransform()
    })
    
    document.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false
        container.style.cursor = 'grab'
      }
    })
    
    // Touch support
    let lastTouchDist = 0
    container.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        isDragging = true
        startX = e.touches[0].clientX - posX
        startY = e.touches[0].clientY - posY
      } else if (e.touches.length === 2) {
        lastTouchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        )
      }
    }, { passive: true })
    
    container.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && isDragging) {
        posX = e.touches[0].clientX - startX
        posY = e.touches[0].clientY - startY
        updateTransform()
      } else if (e.touches.length === 2) {
        e.preventDefault()
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        )
        if (lastTouchDist > 0) {
          scale = Math.max(0.25, Math.min(4, scale * (dist / lastTouchDist)))
          updateTransform()
        }
        lastTouchDist = dist
      }
    }, { passive: false })
    
    container.addEventListener('touchend', () => {
      isDragging = false
      lastTouchDist = 0
    })
    
    function updateTransform() {
      container.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`
    }
    
    // Set initial cursor
    container.style.cursor = 'grab'
  })
}
