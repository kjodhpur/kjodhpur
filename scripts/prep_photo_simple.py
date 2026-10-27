#!/usr/bin/env python3
"""Lightweight photo prep (Pillow only) for make_ascii_svg.py — no rembg."""
import sys
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

inp = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
out = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
im = Image.open(inp).convert("RGB")
w, h = im.size
s = min(w, h)
im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
im = im.resize((800, 800), Image.LANCZOS)
g = ImageOps.grayscale(im)
g = ImageEnhance.Contrast(g).enhance(1.35)
g = ImageEnhance.Brightness(g).enhance(1.08)
g = g.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
g.save(out)
print("wrote", out, g.size)
