"""
Generate menu bar icons for different states
Creates simple colored icons for idle, tracking, flow, and error states
"""

from PIL import Image, ImageDraw
from pathlib import Path


def create_menu_icon(color: tuple, output_path: str, size: int = 22):
    """Create a simple circular menu bar icon"""
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    padding = 3
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=color,
        outline=None
    )
    
    # Save
    img.save(output_path, 'PNG')
    print(f"Created {output_path}")


def create_retina_icon(color: tuple, output_path: str):
    """Create retina (2x) version"""
    create_menu_icon(color, output_path, size=44)


def main():
    """Generate all menu bar icons"""
    assets_dir = Path(__file__).parent
    menu_icons_dir = assets_dir / 'menu_icons'
    menu_icons_dir.mkdir(exist_ok=True)
    
    # Color definitions (RGB)
    colors = {
        'idle': (107, 114, 128),      # Gray
        'tracking': (77, 229, 255),   # Cyan
        'flow': (47, 230, 193),       # Teal
        'error': (255, 110, 199),     # Magenta
    }
    
    # Generate icons
    for state, color in colors.items():
        # Standard resolution
        create_menu_icon(color, str(menu_icons_dir / f'{state}.png'), size=22)
        
        # Retina resolution
        create_retina_icon(color, str(menu_icons_dir / f'{state}@2x.png'))
    
    print("\nAll menu bar icons generated successfully!")


if __name__ == '__main__':
    main()
