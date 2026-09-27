import os
import io
import json
import shutil
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
LOCAL_PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')

def load_config():
    """Load configuration from config.json with strict validation"""
    config_path = os.path.join(BASE_DIR, 'config.json')
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found!")
        print("   Please create config.json with your details.")
        sys.exit(1)
        
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    if 'google_drive_folder_id' not in config:
        print(f"Error: 'google_drive_folder_id' missing in {config_path}")
        sys.exit(1)
        
    return config

# Load parent folder ID from config
config = load_config()
PARENT_FOLDER_ID = config['google_drive_folder_id']
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticates using the Service Account."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found!")
        print("   Please ensure your Google Drive credentials file exists.")
        return None
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def get_folders(service, parent_id):
    """Gets subfolders inside a given parent folder."""
    query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def get_images(service, folder_id):
    """Gets images and videos inside a specific folder."""
    query = f"'{folder_id}' in parents and (mimeType contains 'image/' or mimeType contains 'video/') and trashed = false"
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
        print(f"   Warning: Error downloading: {e}")
        return False

def sync_flat_folder(service, category_id, local_category_path, drive_links,
                     total_downloaded, total_skipped, indent="   "):
    """Syncs images from a single flat Google Drive folder into a local directory."""
    images = get_images(service, category_id)
    drive_image_names = [img['name'] for img in images]

    # Two-way sync: remove stale local files
    if os.path.exists(local_category_path):
        for local_file in os.listdir(local_category_path):
            local_file_path = os.path.join(local_category_path, local_file)
            if os.path.isfile(local_file_path) and local_file not in drive_image_names:
                print(f"{indent}Removing deleted image: {local_file}")
                os.remove(local_file_path)

    for image in images:
        image_name = image['name']
        drive_links[image_name] = image.get('webViewLink', '')
        local_image_path = os.path.join(local_category_path, image_name)

        if os.path.exists(local_image_path):
            print(f"{indent}  (already exists) {image_name}")
            total_skipped += 1
            continue

        print(f"{indent}Downloading {image_name}... ", end='', flush=True)
        if download_file(service, image['id'], local_image_path):
            print("done")
            total_downloaded += 1
        else:
            print("FAILED")

    return total_downloaded, total_skipped

def sync_photos():
    """Main sync function - downloads all photos from Google Drive."""
    print("Google Drive Photo Sync")
    print("=" * 50)
    print()
    
    # Authenticate
    service = authenticate()
    if not service:
        return
    
    print(f"Connected to Google Drive")
    print(f"Parent Folder ID: {PARENT_FOLDER_ID}")
    print()
    
    # Create local photos directory
    os.makedirs(LOCAL_PHOTOS_DIR, exist_ok=True)
    
    # Link mapping dictionary
    drive_links = {}
    
    # Get all category folders
    folders = get_folders(service, PARENT_FOLDER_ID)
    
    if not folders:
        print("No category folders found in Google Drive!")
        print(f"   Check that folder ID '{PARENT_FOLDER_ID}' is correct or add folders to it.")
        sys.exit(1)
    
    # Two-Way Sync: Cleanup stale top-level categories
    drive_category_names = [f['name'] for f in folders]
    if os.path.exists(LOCAL_PHOTOS_DIR):
        for local_dir in os.listdir(LOCAL_PHOTOS_DIR):
            local_path = os.path.join(LOCAL_PHOTOS_DIR, local_dir)
            if os.path.isdir(local_path) and local_dir not in drive_category_names:
                print(f"Removing deleted category from local storage: {local_dir}")
                shutil.rmtree(local_path)
    
    total_downloaded = 0
    total_skipped = 0
    
    for folder in folders:
        category_name = folder['name']
        category_id = folder['id']
        
        print(f"Category: {category_name}")
        
        local_category_path = os.path.join(LOCAL_PHOTOS_DIR, category_name)
        os.makedirs(local_category_path, exist_ok=True)
        
        # Check for sub-folders (child categories)
        sub_folders = get_folders(service, category_id)
        
        if sub_folders:
            # --- Hierarchical Mode: parent folder has child sub-folders ---
            drive_child_names = [sf['name'] for sf in sub_folders]
            
            # Cleanup stale local child folders
            for local_child in os.listdir(local_category_path):
                local_child_path = os.path.join(local_category_path, local_child)
                if os.path.isdir(local_child_path) and local_child not in drive_child_names:
                    print(f"   Removing deleted sub-folder: {local_child}")
                    shutil.rmtree(local_child_path)
            
            # Sync any images placed directly in the parent folder
            parent_images = get_images(service, category_id)
            drive_parent_image_names = [img['name'] for img in parent_images]
            for local_file in os.listdir(local_category_path):
                local_file_path = os.path.join(local_category_path, local_file)
                if os.path.isfile(local_file_path) and local_file not in drive_parent_image_names:
                    print(f"   Removing deleted image from parent: {local_file}")
                    os.remove(local_file_path)
            
            for image in parent_images:
                image_name = image['name']
                drive_links[image_name] = image.get('webViewLink', '')
                local_image_path = os.path.join(local_category_path, image_name)
                if os.path.exists(local_image_path):
                    print(f"   (already exists) {image_name}")
                    total_skipped += 1
                    continue
                print(f"   Downloading {image_name}... ", end='', flush=True)
                if download_file(service, image['id'], local_image_path):
                    print("done")
                    total_downloaded += 1
                else:
                    print("FAILED")
            
            # Process each child sub-folder
            for sub_folder in sub_folders:
                child_name = sub_folder['name']
                child_id = sub_folder['id']
                print(f"   Sub-folder: {child_name}")
                
                local_child_path = os.path.join(local_category_path, child_name)
                os.makedirs(local_child_path, exist_ok=True)
                
                total_downloaded, total_skipped = sync_flat_folder(
                    service, child_id, local_child_path, drive_links,
                    total_downloaded, total_skipped, indent="      "
                )
        
        else:
            # --- Flat Mode: no sub-folders, sync images directly ---
            total_downloaded, total_skipped = sync_flat_folder(
                service, category_id, local_category_path, drive_links,
                total_downloaded, total_skipped, indent="   "
            )
        
        print()
    
    # Save drive links
    with open('drive_links.json', 'w') as f:
        json.dump(drive_links, f, indent=4)
    print(f"Saved drive links to drive_links.json")

    print("=" * 50)
    print(f"Sync Complete!")
    print(f"   Downloaded: {total_downloaded} images")
    print(f"   Skipped: {total_skipped} images (already exist)")
    print()
    print(f"Photos saved to: {LOCAL_PHOTOS_DIR}/")
    print()

if __name__ == '__main__':
    sync_photos()
