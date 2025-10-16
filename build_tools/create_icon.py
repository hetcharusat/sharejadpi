"""
Generate ShareJadPi icon file
Creates a green sphere icon for the application
"""
from PIL import Image, ImageDraw

def create_icon():
    """Create a professional green sphere icon"""
    # Create a larger image for better quality (256x256)
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw green gradient sphere
    center = size // 2
    radius = size // 2 - 10
    
    # Main green circle
    draw.ellipse(
        [(center - radius, center - radius), (center + radius, center + radius)],
        fill=(76, 175, 80, 255)  # Material green
    )
    
    # Highlight for 3D effect (top-left)
    highlight_radius = int(radius * 0.3)
    highlight_offset_x = int(radius * 0.3)
    highlight_offset_y = int(radius * 0.3)
    draw.ellipse(
        [(center - highlight_offset_x - highlight_radius, center - highlight_offset_y - highlight_radius),
         (center - highlight_offset_x + highlight_radius, center - highlight_offset_y + highlight_radius)],
        fill=(144, 238, 144, 150)  # Light green with transparency
    )
    
    # Save as ICO with multiple sizes
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✓ Created icon.ico")
    
    # Also save as PNG for reference
    img.save('icon.png', format='PNG')
    print("✓ Created icon.png")

if __name__ == '__main__':
    create_icon()
