#!/usr/bin/env python3
"""
Image Optimization Script
Compresses and resizes images for web delivery.
Supports both flat category folders and nested category/sub-category hierarchies.
"""

import os
import shutil
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
ENABLE_OPTIMIZATION = True   # Enable to convert HEIC -> JPG for browsers
MAX_WIDTH = 4000             # Keep large dimensions
MAX_HEIGHT = 4000            # Keep large dimensions
JPEG_QUALITY = 95            # 95% quality (minimal loss)
PRESERVE_FORMAT = False      # Convert all to JPG for browser compatibility

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp', '.gif', '.mp4', '.mov', '.webm', '.m4v'}
VIDEO_FORMATS = {'.mp4', '.mov', '.webm', '.m4v'}


def optimize_video(input_path, output_path):
    """Compress video for fast web delivery using hardware acceleration (keeping under 25MB limit)"""
    try:
        import subprocess
        if shutil.which('avconvert'):
            cmd = [
                'avconvert',
                '-s', input_path,
                '-p', 'Preset640x480',
                '--duration', '25',
                '-o', output_path,
                '--replace'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and os.path.exists(output_path):
                return True
    except Exception as e:
        print(f"   Warning: video optimization fallback: {e}")

    shutil.copy2(input_path, output_path)
    return True


def optimize_image(input_path, output_path):
    """Optimize a single image or video"""
    try:
        ext = os.path.splitext(input_path.lower())[1]

        if ext in VIDEO_FORMATS:
            return optimize_video(input_path, output_path)

        if ext == '.gif' or not ENABLE_OPTIMIZATION:
            shutil.copy2(input_path, output_path)
            return True
        
        with Image.open(input_path) as img:
            # Determine output format
            if PRESERVE_FORMAT:
                output_format = img.format if img.format in ['JPEG', 'PNG', 'WEBP'] else 'JPEG'
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
        print(f"   Warning: Failed to process {input_path}: {e}")
        return False


def process_folder(input_folder, output_folder, label="", total_counts=None):
    """
    Recursively processes a folder, handling both flat images and sub-folders.
    Returns (processed, skipped) counts.
    """
    if total_counts is None:
        total_counts = {'processed': 0, 'skipped': 0}

    os.makedirs(output_folder, exist_ok=True)

    entries = sorted(os.listdir(input_folder))

    for entry in entries:
        input_path = os.path.join(input_folder, entry)
        output_path_base = os.path.join(output_folder, entry)

        if os.path.isdir(input_path):
            # Recurse into sub-folder
            indent = "   " if label else ""
            print(f"{indent}Sub-folder: {entry}")
            process_folder(input_path, output_path_base,
                           label=entry, total_counts=total_counts)

        elif os.path.isfile(input_path):
            ext = os.path.splitext(entry.lower())[1]
            if ext not in SUPPORTED_FORMATS:
                continue

            # Determine output filename
            if ext in VIDEO_FORMATS or ext == '.gif':
                output_filename = entry
            elif ENABLE_OPTIMIZATION and not PRESERVE_FORMAT:
                output_filename = os.path.splitext(entry)[0] + '.jpg'
            else:
                output_filename = entry

            output_path = os.path.join(output_folder, output_filename)

            # Skip if already processed and newer than source
            if os.path.exists(output_path):
                if os.path.getmtime(output_path) > os.path.getmtime(input_path):
                    total_counts['skipped'] += 1
                    continue

            if optimize_image(input_path, output_path):
                print(f"   ✓ {entry}")
                total_counts['processed'] += 1
            else:
                total_counts['skipped'] += 1

    return total_counts


def cleanup_stale_cache(input_root, output_root):
    """
    Two-way sync: remove anything from output that no longer exists in input.
    Handles both top-level categories and nested sub-folders.
    """
    if not os.path.exists(output_root):
        return

    input_entries = set(os.listdir(input_root)) if os.path.exists(input_root) else set()

    for opt_entry in os.listdir(output_root):
        opt_path = os.path.join(output_root, opt_entry)

        if os.path.isdir(opt_path):
            if opt_entry not in input_entries:
                print(f"Removing deleted category from optimized cache: {opt_entry}")
                shutil.rmtree(opt_path)
            else:
                # Recurse into sub-folder to clean up stale children
                input_sub = os.path.join(input_root, opt_entry)
                cleanup_stale_cache(input_sub, opt_path)

        elif os.path.isfile(opt_path):
            # Match by stem (handle extension changes like HEIC -> jpg)
            opt_stem = os.path.splitext(opt_entry)[0]
            input_stems = {os.path.splitext(f)[0] for f in input_entries if os.path.isfile(os.path.join(input_root, f))}
            if opt_stem not in input_stems:
                print(f"   Removing deleted image from cache: {opt_entry}")
                os.remove(opt_path)


def process_all_images():
    """Process all images in the photos directory, supporting nested sub-folders."""
    print("Starting image optimization...")
    print(f"   Input:  {INPUT_DIR}")
    print(f"   Output: {OUTPUT_DIR}")

    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found!")
        print("   Please run 'python scripts/sync_from_drive.py' first.")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean up stale cache entries recursively
    cleanup_stale_cache(INPUT_DIR, OUTPUT_DIR)

    if ENABLE_OPTIMIZATION:
        print(f"   Quality: {JPEG_QUALITY}%")
        print(f"   Max Size: {MAX_WIDTH}x{MAX_HEIGHT}px")
    else:
        print("   Mode: FULL QUALITY (No compression)")
    print()

    total_counts = {'processed': 0, 'skipped': 0}

    # Process each top-level category folder
    for category in sorted(os.listdir(INPUT_DIR)):
        category_path = os.path.join(INPUT_DIR, category)

        if not os.path.isdir(category_path):
            continue

        print(f"Category: {category}")
        output_category_path = os.path.join(OUTPUT_DIR, category)

        process_folder(category_path, output_category_path,
                       label=category, total_counts=total_counts)

    print()
    print(f"Optimization Complete!")
    print(f"   Processed: {total_counts['processed']} images")
    print(f"   Skipped: {total_counts['skipped']} images (already processed)")


if __name__ == '__main__':
    process_all_images()
