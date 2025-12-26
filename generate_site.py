#!/usr/bin/env python3
"""
Static Site Generator for Photography Portfolio
Scans local photo folders and generates data.json + website files
"""

import os
import json
import shutil
from pathlib import Path

# Configuration
PHOTOS_DIR = "optimized"  # Use optimized images
SITE_DIR = "site"
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif'}

def scan_photos():
    """Scan photo directories and build portfolio data structure"""
    portfolio_data = {"tabs": []}
    
    if not os.path.exists(PHOTOS_DIR):
        print(f"⚠️  Warning: '{PHOTOS_DIR}' directory not found!")
        print(f"   Run 'python optimize_images.py' first to create optimized images.")
        return portfolio_data
    
    # Get all category folders
    categories = [d for d in os.listdir(PHOTOS_DIR) 
                 if os.path.isdir(os.path.join(PHOTOS_DIR, d)) and not d.startswith('.')]
    
    print("📸 Scanning Photo Folders...")
    
    for category in sorted(categories):
        category_path = os.path.join(PHOTOS_DIR, category)
        
        print(f"   📂 {category}")
        
        # Get all images in this category
        images = []
        for file in sorted(os.listdir(category_path)):
            file_path = os.path.join(category_path, file)
            
            if os.path.isfile(file_path):
                ext = os.path.splitext(file.lower())[1]
                if ext in SUPPORTED_FORMATS:
                    # Store relative path from site directory
                    relative_path = f"../{PHOTOS_DIR}/{category}/{file}"
                    images.append({
                        "name": file,
                        "path": relative_path
                    })
        
        if images:
            portfolio_data["tabs"].append({
                "category": category,
                "images": images
            })
            print(f"      ✓ {len(images)} images")
        else:
            print(f"      ⚠️  No images found")
    
    return portfolio_data

def setup_site_directory():
    """Create site directory if it doesn't exist"""
    os.makedirs(SITE_DIR, exist_ok=True)

def generate_data_json(portfolio_data):
    """Generate data.json file"""
    output_path = os.path.join(SITE_DIR, 'data.json')
    
    with open(output_path, 'w') as f:
        json.dump(portfolio_data, f, indent=2)
    
    print(f"✅ Generated: {output_path}")

def copy_frontend_files():
    """Copy HTML, CSS, JS files to site directory"""
    files_to_copy = ['index.html', 'style.css', 'script.js']
    
    print("\n📋 Copying Frontend Files...")
    
    for file in files_to_copy:
        if os.path.exists(file):
            dest = os.path.join(SITE_DIR, file)
            shutil.copy2(file, dest)
            print(f"   ✓ {file}")
        else:
            print(f"   ⚠️  {file} not found - skipping")

def create_gitignore():
    """Create .gitignore for the project"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# Optimized images (can be regenerated)
optimized/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Old backup
old_google_drive_version/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print(f"✅ Created: .gitignore")

def main():
    """Main site generation process"""
    print("🚀 Portfolio Site Generator")
    print("=" * 50)
    print()
    
    # Scan photos and build data structure
    portfolio_data = scan_photos()
    
    if not portfolio_data["tabs"]:
        print("\n❌ No photos found!")
        print("   1. Add photos to folders inside 'photos/' directory")
        print("   2. Run: python optimize_images.py")
        print("   3. Run: python generate_site.py")
        return
    
    print()
    
    # Create site directory
    setup_site_directory()
    
    # Generate data.json
    generate_data_json(portfolio_data)
    
    # Copy frontend files
    copy_frontend_files()
    
    # Create .gitignore
    create_gitignore()
    
    print()
    print("=" * 50)
    print("✨ Site Generated Successfully!")
    print()
    print(f"📊 Summary:")
    print(f"   Categories: {len(portfolio_data['tabs'])}")
    total_images = sum(len(tab['images']) for tab in portfolio_data['tabs'])
    print(f"   Total Images: {total_images}")
    print()
    print("🌐 To view your site:")
    print(f"   python -m http.server 8000 --directory {SITE_DIR}")
    print("   Then visit: http://localhost:8000")
    print()

if __name__ == '__main__':
    main()
