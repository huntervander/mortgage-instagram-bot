"""
Composite a generated background image with the brand footer bar:
circular headshot + name/NMLS text on the left, Fairway Independent
Mortgage logo on the right.

Usage:
    python composite_post.py --background-url "https://..." --output "pending/draft_001/image.png"
"""

import argparse
import io
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).parent / "assets"
HEADSHOT_PATH = ASSETS_DIR / "shane_headshot.png"
LOGO_PATH = ASSETS_DIR / "fairway_logo.jpg"

NAME_TEXT = "Shane Vanderleelie"
NMLS_TEXT = "NMLS #2682924"

FOOTER_HEIGHT_RATIO = 0.14  # footer bar height as a fraction of image width


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_circle(img: Image.Image, size: int) -> Image.Image:
    img = img.convert("RGBA")
    # crop to square (center crop)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def composite(background_path_or_url: str, output_path: Path) -> None:
    if background_path_or_url.startswith("http"):
        resp = requests.get(background_path_or_url)
        resp.raise_for_status()
        bg = Image.open(io.BytesIO(resp.content)).convert("RGBA")
    else:
        bg = Image.open(background_path_or_url).convert("RGBA")

    w, h = bg.size
    footer_h = int(w * FOOTER_HEIGHT_RATIO)

    # Extend canvas downward and draw a dark footer bar
    canvas = Image.new("RGBA", (w, h + footer_h), (255, 255, 255, 255))
    canvas.paste(bg, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, h, w, h + footer_h), fill=(20, 30, 48, 255))  # dark navy bar

    # Headshot circle on the left
    margin = int(footer_h * 0.12)
    circle_size = footer_h - 2 * margin
    headshot = make_circle(Image.open(HEADSHOT_PATH), circle_size)
    headshot_pos = (margin, h + margin)
    canvas.paste(headshot, headshot_pos, headshot)

    # White ring around headshot
    ring_draw = ImageDraw.Draw(canvas)
    ring_draw.ellipse(
        (headshot_pos[0] - 3, headshot_pos[1] - 3,
         headshot_pos[0] + circle_size + 3, headshot_pos[1] + circle_size + 3),
        outline=(255, 255, 255, 255), width=3,
    )

    # Name + NMLS text next to headshot
    text_x = headshot_pos[0] + circle_size + margin
    name_font = load_font(int(footer_h * 0.28))
    nmls_font = load_font(int(footer_h * 0.18))

    name_y = h + margin + int(footer_h * 0.05)
    nmls_y = name_y + int(footer_h * 0.36)

    draw.text((text_x, name_y), NAME_TEXT, fill=(255, 255, 255, 255), font=name_font)
    draw.text((text_x, nmls_y), NMLS_TEXT, fill=(200, 200, 200, 255), font=nmls_font)

    # Fairway logo on the right
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = footer_h - 2 * margin
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_pos = (w - margin - logo_size, h + margin)
    canvas.paste(logo, logo_pos, logo)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--background-url", required=True, help="URL or local path of generated background image")
    parser.add_argument("--output", required=True, help="Output file path")
    args = parser.parse_args()
    composite(args.background_url, Path(args.output))


if __name__ == "__main__":
    main()
