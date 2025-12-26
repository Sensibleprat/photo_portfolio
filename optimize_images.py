#!/usr/bin/env python3
"""
Image Optimization Script
Compresses and resizes images for web delivery
"""

import os
from PIL import Image
from pathlib import Path

# Configuration
SOURCE_DIR = "photos"
OUTPUT_DIR = "optimized"
MAX_WIDTH = 2000
MAX_HEIGHT = 2000
JPEG_QUALITY = 85
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
    """Optimize a single image"""
    try:
        # Open image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if necessary (for JPEG)
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
            img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to optimize {input_path}: {e}")
        return False

def process_all_images():
    """Process all images in the photos directory"""
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: '{SOURCE_DIR}' directory not found!")
        print(f"   Please create a '{SOURCE_DIR}' folder and add your photo categories inside it.")
        return
    
    setup_directories()
    
    print("🎨 Starting Image Optimization...")
    print(f"   Source: {SOURCE_DIR}/")
    print(f"   Output: {OUTPUT_DIR}/")
    print()
    
    total_processed = 0
    total_skipped = 0
    
    # Walk through all categories
    for category in sorted(os.listdir(SOURCE_DIR)):
        category_path = os.path.join(SOURCE_DIR, category)
        
        if not os.path.isdir(category_path):
            continue
        
        print(f"📂 Processing: {category}")
        
        output_category_path = os.path.join(OUTPUT_DIR, category)
        
        # Process all images in this category
        images = [f for f in os.listdir(category_path) 
                 if os.path.splitext(f.lower())[1] in SUPPORTED_FORMATS]
        
        for image_file in sorted(images):
            input_path = os.path.join(category_path, image_file)
            
            # Change extension to .jpg for output
            output_filename = os.path.splitext(image_file)[0] + '.jpg'
            output_path = os.path.join(output_category_path, output_filename)
            
            # Skip if already optimized and newer than source
            if os.path.exists(output_path):
                if os.path.getmtime(output_path) > os.path.getmtime(input_path):
                    total_skipped += 1
                    continue
            
            # Optimize the image
            if optimize_image(input_path, output_path):
                print(f"   ✓ {image_file}")
                total_processed += 1
            else:
                total_skipped += 1
    
    print()
    print(f"✅ Optimization Complete!")
    print(f"   Processed: {total_processed} images")
    print(f"   Skipped: {total_skipped} images (already optimized)")

if __name__ == '__main__':
    process_all_images()
