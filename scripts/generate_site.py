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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(BASE_DIR, 'optimized')  # Use optimized images
SITE_DIR = os.path.join(BASE_DIR, 'site')
SRC_DIR = os.path.join(BASE_DIR, 'src')
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp'}  # Excluding HEIC - converted to JPG

def load_config():
    """Load user configuration with strict validation"""
    config_path = os.path.join(BASE_DIR, 'config.json')
    
    if not os.path.exists(config_path):
        print(f"❌ Error: {config_path} not found!")
        print("   Please create config.json with your details.")
        exit(1)
        
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    # Strict validation - ensure required fields exist
    required_fields = ["name", "handle", "instagram_url"]
    missing_fields = [field for field in required_fields if field not in config]
    
    if missing_fields:
        print(f"❌ Error: Missing required fields in {config_path}:")
        for field in missing_fields:
            print(f"   - {field}")
        exit(1)
        
    return config

def load_drive_links():
    """Load Google Drive link mapping"""
    links_path = os.path.join(BASE_DIR, 'drive_links.json')
    if os.path.exists(links_path):
        with open(links_path, 'r') as f:
            return json.load(f)
    return {}

def scan_photos(drive_links):
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
                    # Store relative path within site directory
                    # Images will be copied to site/images/
                    relative_path = f"images/{category}/{file}"
                    
                    # Original filename logic to match drive_links keys
                    drive_url = drive_links.get(file, "")
                    
                    # If conversion changed extension (HEIC -> jpg), try to find original key
                    if not drive_url:
                        base_name = os.path.splitext(file)[0]
                        for link_name, link_url in drive_links.items():
                            if os.path.splitext(link_name)[0] == base_name:
                                drive_url = link_url
                                break
                    
                    images.append({
                        "name": file,
                        "path": relative_path,
                        "drive_url": drive_url
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

def copy_frontend_files(config):
    """Copy and template HTML, CSS, JS files to site directory"""
    print("\n📋 Processing Frontend Files...")
    
    # Process index.html with config substitutions
    index_path = os.path.join(SRC_DIR, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            content = f.read()
        
        # Substitute placeholders
        content = content.replace('Your Name', config['name'])
        
        # Hyperlink the handle using config URL
        handle = config['handle']
        insta_url = config['instagram_url']
        
        if insta_url:
             linked_handle = f'<a href="{insta_url}" target="_blank" style="text-decoration: none; color: inherit;">{handle}</a>'
             content = content.replace('@YourHandle', linked_handle)
        else:
             content = content.replace('@YourHandle', handle)
        
        # Handle profile picture
        profile_pic_filename = config.get('profile_picture')
        if profile_pic_filename and os.path.exists(f"../photos/{profile_pic_filename}"):
            # Using style injection for background image
            css_injection = f"""<style>
                .profile-image {{
                    background-image: url('images/{profile_pic_filename}');
                    background-size: cover;
                    background-position: center;
                }}
                .profile-image::before {{ content: none !important; }}
            </style>
            </head>"""
            content = content.replace('</head>', css_injection)
        
        with open(os.path.join(SITE_DIR, 'index.html'), 'w') as f:
            f.write(content)
        print("   ✓ index.html (customized)")

    # Copy other files directly
    for file in ['style.css', 'script.js']:
        src_file = os.path.join(SRC_DIR, file)
        if os.path.exists(src_file):
            dest = os.path.join(SITE_DIR, file)
            shutil.copy2(src_file, dest)
            print(f"   ✓ {file}")
        else:
            print(f"   ⚠️  {file} not found - skipping")

def copy_images(config):
    """Copy optimized images and profile pic to site/images/ directory"""
    images_dir = os.path.join(SITE_DIR, 'images')
    
    print("\n📸 Copying Images to Site...")
    
    if not os.path.exists(PHOTOS_DIR):
        print(f"   ⚠️  {PHOTOS_DIR}/ not found - skipping")
        return
    
    # Create images directory
    os.makedirs(images_dir, exist_ok=True)
    
    total_copied = 0
    
    # Copy all category folders
    for category in os.listdir(PHOTOS_DIR):
        category_src = os.path.join(PHOTOS_DIR, category)
        
        if not os.path.isdir(category_src):
            continue
        
        category_dest = os.path.join(images_dir, category)
        
        # Copy entire category folder
        if os.path.exists(category_dest):
            shutil.rmtree(category_dest)
        shutil.copytree(category_src, category_dest)
        
        # Count images
        images = [f for f in os.listdir(category_dest) 
                 if os.path.splitext(f.lower())[1] in SUPPORTED_FORMATS]
        total_copied += len(images)
        print(f"   ✓ {category}: {len(images)} images")
    
    # Copy profile picture
    profile_pic = config.get('profile_picture')
    if profile_pic:
        src = os.path.join('../photos', profile_pic)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(images_dir, profile_pic))
            print(f"   ✓ Profile picture copied: {profile_pic}")
        else:
             print(f"   ⚠️ Profile picture not found at: {src}")

    print(f"\n   Total: {total_copied} images copied to site/")

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

# Downloaded photos (synced from Google Drive)
photos/*
!photos/README.md

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
.AppleDouble
.LSOverride

# Old backup
old_google_drive_version/

# Credentials (NEVER commit these!)
credentials.json
token.json
*.json
!package.json
!data.json
!site/data.json
!config.json
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print(f"✅ Created: .gitignore")

def main():
    """Main site generation process"""
    print("🚀 Portfolio Site Generator")
    print("=" * 50)
    print()
    
    # Load Config and Drive Links
    config = load_config()
    drive_links = load_drive_links()
    print(f"👤 Customizing for: {config.get('name')}")
    
    # Scan photos and build data structure
    portfolio_data = scan_photos(drive_links=drive_links)
    
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
    
    # Copy frontend files (with customization)
    copy_frontend_files(config)
    
    # Copy images to site directory
    copy_images(config)
    
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
