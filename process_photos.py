"""
KOALA PRESCHOOL — Photo Processor
===================================
Removes background + crops to shoulder length for all student photos.

Usage:
    1. Put all raw photos in a folder called: raw_photos/
    2. Run: python3 process_photos.py
    3. Get processed photos from: processed_photos/

Processed photos are ready to upload directly to the ID card generator app.
"""

import os
import sys
from pathlib import Path
from PIL import Image
from rembg import remove

# ── Config ──────────────────────────────────────────────────────────────
INPUT_DIR  = Path("raw_photos")        # folder with original photos
OUTPUT_DIR = Path("processed_photos")  # folder for processed output
CROP_PCT   = 0.68                      # keep top 68% = head + shoulders + collar
SUPPORTED  = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"}

# ── Setup ────────────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(exist_ok=True)

if not INPUT_DIR.exists():
    INPUT_DIR.mkdir()
    print(f"📁 Created '{INPUT_DIR}/' folder.")
    print(f"   Put your student photos in there, then run this script again.")
    sys.exit(0)

photos = [f for f in INPUT_DIR.iterdir() if f.suffix in SUPPORTED]

if not photos:
    print(f"❌ No photos found in '{INPUT_DIR}/'")
    print(f"   Add photos and run again.")
    sys.exit(0)

photos.sort()  # alphabetical order = matches Excel row order
print(f"🐨 Koala Photo Processor")
print(f"=" * 40)
print(f"Found {len(photos)} photo(s) in {INPUT_DIR}/\n")

# ── Process each photo ───────────────────────────────────────────────────
for i, photo_path in enumerate(photos, 1):
    print(f"[{i}/{len(photos)}] {photo_path.name}...")

    try:
        # Load original
        img = Image.open(photo_path).convert("RGBA")
        w, h = img.size

        # Step 1: Crop to shoulder length (top 68%)
        crop_h = int(h * CROP_PCT)
        img_cropped = img.crop((0, 0, w, crop_h))

        # Step 2: Remove background using rembg AI
        img_bytes = img_cropped.tobytes()
        
        # Convert to bytes for rembg
        import io
        buf = io.BytesIO()
        img_cropped.save(buf, format="PNG")
        buf.seek(0)
        
        result_bytes = remove(buf.read())
        result_img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

        # Step 3: Save with same name (always PNG to preserve transparency)
        out_name = photo_path.stem + ".png"
        out_path = OUTPUT_DIR / out_name
        result_img.save(out_path, "PNG")

        print(f"   ✅ Saved: {out_name}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n✅ Done! {len(photos)} photo(s) processed.")
print(f"   Upload everything from '{OUTPUT_DIR}/' to the ID card generator app.")
print(f"   Photos are sorted alphabetically — upload them in this order to match Excel rows.")