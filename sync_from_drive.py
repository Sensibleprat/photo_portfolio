#!/usr/bin/env python3
"""
Google Drive Photo Sync Script
Downloads photos from Google Drive to local photos/ directory
"""

import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Configuration
PARENT_FOLDER_ID = '1KtAZreDObnIKpNf-Z-HYMFIjfiejqRp-'  # Your Google Drive folder ID
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'old_google_drive_version/credentials.json'
LOCAL_PHOTOS_DIR = 'photos'

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
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    fields = "files(id, name, mimeType)"
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
    
    print("=" * 50)
    print(f"✅ Sync Complete!")
    print(f"   Downloaded: {total_downloaded} images")
    print(f"   Skipped: {total_skipped} images (already exist)")
    print()
    print(f"📁 Photos saved to: {LOCAL_PHOTOS_DIR}/")
    print()

if __name__ == '__main__':
    sync_photos()
