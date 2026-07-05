from PIL import Image, ImageDraw, ImageFont
import os

# Base icon size and colors
BASE_SIZE = 1024
BG_COLOR = (18, 18, 18, 255)
FG_COLOR = (255, 255, 255, 255)

# Create base image with dark background
base = Image.new("RGBA", (BASE_SIZE, BASE_SIZE), BG_COLOR)
draw = ImageDraw.Draw(base)

# Load a bold sans-serif font for the Greek Sigma symbol
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = int(BASE_SIZE * 0.6)
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception:
    font = ImageFont.load_default()

text = "Σ"

# Calculate text position to center it
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (BASE_SIZE - text_width) // 2
# Slight upward adjustment for visual centering
y = (BASE_SIZE - text_height) // 2 - int(BASE_SIZE * 0.05)

# Draw the sigma symbol
draw.text((x, y), text, font=font, fill=FG_COLOR)

# Define Android density icon sizes (square)
sizes = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192
}

# Output directory relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(script_dir, "temp_icons")
os.makedirs(out_dir, exist_ok=True)

for density, size in sizes.items():
    density_dir = os.path.join(out_dir, f"mipmap-{density}")
    os.makedirs(density_dir, exist_ok=True)

    # Create square icon
    square_icon = base.resize((size, size), Image.LANCZOS)
    square_icon.save(os.path.join(density_dir, "ic_launcher.png"))

    # Create circular mask for round icon
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)

    # Apply mask to square icon for round version
    round_icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    round_icon.paste(square_icon, (0, 0), mask=mask)
    round_icon.save(os.path.join(density_dir, "ic_launcher_round.png"))
