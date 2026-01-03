#!/usr/bin/env python3
"""
Image Optimization Script
Compresses and resizes images for web delivery
"""

import os
from PIL import Image
from pathlib import Path
import pillow_heif

# Register HEIC opener with Pillow
pillow_heif.register_heif_opener()

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'photos')
OUTPUT_DIR = os.path.join(BASE_DIR, 'optimized')

# Image Quality Settings
ENABLE_OPTIMIZATION = True   # Enable to convert HEIC → JPG for browsers
MAX_WIDTH = 4000             # Keep large dimensions
MAX_HEIGHT = 4000            # Keep large dimensions
JPEG_QUALITY = 95            # 95% quality (minimal loss)
PRESERVE_FORMAT = False      # Convert all to JPG for browser compatibility

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp'}

def setup_directories():
    """Create output directory structure matching source"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Create subdirectories for each category
    for category in os.listdir(SOURCE_DIR):
        category_path = os.path.join(SOURCE_DIR, category)
        if os.path.isdir(category_path):
            output_category_path = os.path.join(OUTPUT_DIR, category)
            os.makedirs(output_category_path, exist_ok=True)

def optimize_image(input_path, output_path):
    """Optimize a single image (or copy if optimization disabled)"""
    try:
        # If optimization is disabled, just copy the file
        if not ENABLE_OPTIMIZATION:
            import shutil
            shutil.copy2(input_path, output_path)
            return True
        
        # Open image
        with Image.open(input_path) as img:
            # Determine output format
            if PRESERVE_FORMAT:
                output_format = img.format if img.format in ['JPEG', 'PNG', 'WEBP'] else 'JPEG'
                # Update output path extension if needed
                if output_format != 'JPEG':
                    base = os.path.splitext(output_path)[0]
                    ext_map = {'PNG': '.png', 'WEBP': '.webp'}
                    output_path = base + ext_map.get(output_format, '.jpg')
            else:
                output_format = 'JPEG'
            
            # Convert RGBA to RGB if saving as JPEG
            if output_format == 'JPEG':
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
            
            # Resize if needed
            if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save optimized version
            save_kwargs = {'optimize': True}
            if output_format == 'JPEG':
                save_kwargs['quality'] = JPEG_QUALITY
            
            img.save(output_path, output_format, **save_kwargs)
            
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to process {input_path}: {e}")
        return False

def process_all_images():
    """Process all images in the photos directory"""

    mode_text = "Copying Images (Full Quality)" if not ENABLE_OPTIMIZATION else "Optimizing Images"
    print(f"🚀 Starting image optimization...")
    print(f"   Input:  {INPUT_DIR}")
    print(f"   Output: {OUTPUT_DIR}")
    
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: Input directory '{INPUT_DIR}' not found!")
        print(f"   Please run 'python scripts/sync_from_drive.py' first.")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total_images = 0
    
    if ENABLE_OPTIMIZATION:
        print(f"   Quality: {JPEG_QUALITY}%")
        print(f"   Max Size: {MAX_WIDTH}x{MAX_HEIGHT}px")
    else:
        print(f"   Mode: FULL QUALITY (No compression)")
    print()
    
    total_processed = 0
    total_skipped = 0
    
    # Process each category folder
    for category in sorted(os.listdir(INPUT_DIR)):
        category_path = os.path.join(INPUT_DIR, category)
        
        if not os.path.isdir(category_path):
            continue
        
        print(f"📂 Processing: {category}")
        
        output_category_path = os.path.join(OUTPUT_DIR, category)
        
        # Process all images in this category
        images = [f for f in os.listdir(category_path) 
                 if os.path.splitext(f.lower())[1] in SUPPORTED_FORMATS]
        
        for image_file in sorted(images):
            input_path = os.path.join(category_path, image_file)
            
            # Determine output filename
            if ENABLE_OPTIMIZATION and not PRESERVE_FORMAT:
                output_filename = os.path.splitext(image_file)[0] + '.jpg'
            else:
                output_filename = image_file
            
            output_path = os.path.join(output_category_path, output_filename)
            
            # Skip if already processed and newer than source
            if os.path.exists(output_path):
                if os.path.getmtime(output_path) > os.path.getmtime(input_path):
                    total_skipped += 1
                    continue
            
            # Process the image
            if optimize_image(input_path, output_path):
                print(f"   ✓ {image_file}")
                total_processed += 1
            else:
                total_skipped += 1
    
    print()
    action_text = "Complete!" if not ENABLE_OPTIMIZATION else "Optimization Complete!"
    print(f"✅ {action_text}")
    print(f"   Processed: {total_processed} images")
    print(f"   Skipped: {total_skipped} images (already processed)")

if __name__ == '__main__':
    process_all_images()
