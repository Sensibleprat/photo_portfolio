import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 1. Configuration - REPLACE THIS ID
PARENT_FOLDER_ID = '1KtAZreDObnIKpNf-Z-HYMFIjfiejqRp-' 
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def authenticate():
    """Authenticates using the Service Account."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def get_folders(service, parent_id):
    """Finds subfolders (your Tabs: Nature, Street, etc.)"""
    query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def get_images(service, folder_id):
    """Finds images inside a specific folder, requesting only ID and name."""
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    # CRITICAL: Only request ID and Name to avoid requesting problematic API links
    fields = "files(id, name)"
    results = service.files().list(q=query, fields=fields).execute()
    return results.get('files', [])

def main():
    service = authenticate()
    portfolio_data = {"tabs": []}

    print("🚀 Starting Portfolio Build...")
    
    tabs = get_folders(service, PARENT_FOLDER_ID)
    
    for tab in tabs:
        print(f"   📂 Processing Tab: {tab['name']}")
        
        images = get_images(service, tab['id'])
        
        image_list = []
        for img in images:
            file_id = img['id']
            
            # 1. Full-Resolution View Link (For Click-Through)
            view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

            # 2. CRITICAL FINAL FIX: Use the oldest, most permissive embed link format
            # This format is essential for images embedded on arbitrary domains (like localhost)
            thumbnail_link = f"https://drive.google.com/thumbnail?id={file_id}"

            image_list.append({
                "name": img['name'],
                "full_res": view_link, 
                "thumbnail": thumbnail_link
            })
            
        portfolio_data["tabs"].append({
            "category": tab['name'],
            "images": image_list
        })

    # Save the output file used by the frontend
    with open('data.json', 'w') as f:
        json.dump(portfolio_data, f, indent=2)
    
    print("✅ data.json generated successfully!")

if __name__ == '__main__':
    main()