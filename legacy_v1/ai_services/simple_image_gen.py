"""
Simple Image Generator - Creates text-based posters
Works offline, no external API needed!
"""

import os
from datetime import datetime
import textwrap


class SimpleImageGenerator:
    """Create simple text-based posters"""
    
    def __init__(self):
        """Initialize generator"""
        self.output_dir = 'static/generated_assets'
        os.makedirs(self.output_dir, exist_ok=True)
        print("⚠️ Image generation initialized (Pillow-free mode)")
    
    def generate_poster(self, text, theme="default", save_path=None):
        """
        Generate a simple text poster
        
        Args:
            text: Main text to display
            theme: Color theme (default, blue, purple, green, dark)
            save_path: Where to save
            
        Returns:
            Path to saved image (or None if Pillow not available)
        """
        try:
            # Try to import Pillow
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image (Instagram size)
            width, height = 1080, 1080
            
            # Theme colors
            themes = {
                'default': {'bg': (99, 102, 241), 'text': (255, 255, 255)},
                'blue': {'bg': (6, 182, 212), 'text': (255, 255, 255)},
                'purple': {'bg': (139, 92, 246), 'text': (255, 255, 255)},
                'green': {'bg': (16, 185, 129), 'text': (255, 255, 255)},
                'dark': {'bg': (30, 30, 48), 'text': (255, 255, 255)},
            }
            
            colors = themes.get(theme, themes['default'])
            
            # Create background
            img = Image.new('RGB', (width, height), colors['bg'])
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font, fallback to default
            try:
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "/System/Library/Fonts/Helvetica.ttc",
                    "C:\\Windows\\Fonts\\arialbd.ttf",
                ]
                
                font_large = None
                for font_path in font_paths:
                    try:
                        font_large = ImageFont.truetype(font_path, 80)
                        font_small = ImageFont.truetype(font_path.replace('Bold', '').replace('bd', ''), 40)
                        break
                    except:
                        continue
                
                if not font_large:
                    font_large = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                    
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Wrap text
            wrapped_lines = textwrap.wrap(text, width=15)
            
            # Calculate position
            line_height = 100
            total_height = len(wrapped_lines) * line_height
            y = (height - total_height) // 2
            
            # Draw each line
            for line in wrapped_lines:
                try:
                    bbox = draw.textbbox((0, 0), line, font=font_large)
                    text_width = bbox[2] - bbox[0]
                except:
                    text_width = len(line) * 40
                
                x = (width - text_width) // 2
                
                # Draw text with shadow
                draw.text((x+3, y+3), line, fill=(0, 0, 0), font=font_large)
                draw.text((x, y), line, fill=colors['text'], font=font_large)
                
                y += line_height
            
            # Add branding
            brand_text = "Created with AI ✨"
            try:
                bbox = draw.textbbox((0, 0), brand_text, font=font_small)
                brand_width = bbox[2] - bbox[0]
            except:
                brand_width = len(brand_text) * 20
                
            draw.text(
                ((width - brand_width) // 2, height - 80),
                brand_text,
                fill=colors['text'],
                font=font_small
            )
            
            # Save
            if not save_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = f"{self.output_dir}/poster_{timestamp}.png"
            
            img.save(save_path)
            
            return save_path
            
        except ImportError:
            # Pillow not installed - skip image generation
            print(f"⚠️ Skipping poster generation (Pillow not installed): {text}")
            return None
        except Exception as e:
            print(f"❌ Error creating poster: {e}")
            return None


def create_simple_image_generator():
    """Create simple image generator"""
    return SimpleImageGenerator()


# Test function
if __name__ == "__main__":
    print("Testing Simple Image Generator...")
    try:
        gen = create_simple_image_generator()
        path = gen.generate_poster("Hello World", theme="blue")
        if path:
            print(f"Poster created: {path}")
        else:
            print("Poster generation skipped (Pillow not installed)")
    except Exception as e:
        print(f"Error: {e}")