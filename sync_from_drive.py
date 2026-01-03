import os
import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Configuration
SERVICE_ACCOUNT_FILE = 'credentials.json'
LOCAL_PHOTOS_DIR = 'photos'

def load_config():
    """Load configuration from config.json with strict validation"""
    config_path = 'config.json'
    if not os.path.exists(config_path):
        print(f"❌ Error: {config_path} not found!")
        print("   Please create config.json with your details.")
        exit(1)
        
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    if 'google_drive_folder_id' not in config:
        print(f"❌ Error: 'google_drive_folder_id' missing in {config_path}")
        exit(1)
        
    return config

# Load parent folder ID from config
config = load_config()
PARENT_FOLDER_ID = config['google_drive_folder_id']
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticates using the Service Account."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Error: {SERVICE_ACCOUNT_FILE} not found!")
        print("   Please ensure your Google Drive credentials file exists.")
        return None
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def get_folders(service, parent_id):
    """Gets subfolders (your categories: Nature, Street, etc.)"""
    query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def get_images(service, folder_id):
    """Gets images inside a specific folder."""
    # Modified to include webViewLink
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    fields = "files(id, name, mimeType, webViewLink)"
    results = service.files().list(q=query, fields=fields).execute()
    return results.get('files', [])

def download_file(service, file_id, destination_path):
    """Downloads a file from Google Drive."""
    try:
        request = service.files().get_media(fileId=file_id)
        
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Download the file
        with io.FileIO(destination_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        
        return True
    except Exception as e:
        print(f"   ⚠️  Error downloading: {e}")
        return False

def sync_photos():
    """Main sync function - downloads all photos from Google Drive."""
    print("🔄 Google Drive Photo Sync")
    print("=" * 50)
    print()
    
    # Authenticate
    service = authenticate()
    if not service:
        return
    
    print(f"✅ Connected to Google Drive")
    print(f"📂 Parent Folder ID: {PARENT_FOLDER_ID}")
    print()
    
    # Create local photos directory
    os.makedirs(LOCAL_PHOTOS_DIR, exist_ok=True)
    
    # Link mapping dictionary
    drive_links = {}
    
    # Get all category folders
    folders = get_folders(service, PARENT_FOLDER_ID)
    
    if not folders:
        print("❌ No category folders found in Google Drive!")
        print(f"   Check that folder ID '{PARENT_FOLDER_ID}' is correct.")
        return
    
    total_downloaded = 0
    total_skipped = 0
    
    # Process each category
    for folder in folders:
        category_name = folder['name']
        category_id = folder['id']
        
        print(f"📂 Category: {category_name}")
        
        # Create local category directory
        local_category_path = os.path.join(LOCAL_PHOTOS_DIR, category_name)
        os.makedirs(local_category_path, exist_ok=True)
        
        # Get images in this category
        images = get_images(service, category_id)
        
        for image in images:
            image_name = image['name']
            image_id = image['id']
            # Store the Drive link
            drive_links[image_name] = image.get('webViewLink', '')
            
            local_image_path = os.path.join(local_category_path, image_name)
            
            # Skip if already downloaded
            if os.path.exists(local_image_path):
                print(f"   ⏭️  {image_name} (already exists)")
                total_skipped += 1
                continue
            
            # Download the image
            print(f"   ⬇️  {image_name}... ", end='', flush=True)
            if download_file(service, image_id, local_image_path):
                print("✅")
                total_downloaded += 1
            else:
                print("❌")
        
        print()
    
    # Save drive links
    with open('drive_links.json', 'w') as f:
        json.dump(drive_links, f, indent=4)
    print(f"✅ Saved drive links to drive_links.json")

    print("=" * 50)
    print(f"✅ Sync Complete!")
    print(f"   Downloaded: {total_downloaded} images")
    print(f"   Skipped: {total_skipped} images (already exist)")
    print()
    print(f"📁 Photos saved to: {LOCAL_PHOTOS_DIR}/")
    print()

if __name__ == '__main__':
    sync_photos()
