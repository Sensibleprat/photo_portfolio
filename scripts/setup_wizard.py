#!/usr/bin/env python3
import os
import json
import shutil
import sys
import time

# ANSI color codes for pretty terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_step(text):
    print(f"{Colors.BLUE}{Colors.BOLD}➜ {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.CYAN}{text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, default=None, required=True):
    while True:
        if default:
            formatted_prompt = f"{Colors.BOLD}{prompt}{Colors.ENDC} [{default}]: "
        else:
            formatted_prompt = f"{Colors.BOLD}{prompt}{Colors.ENDC}: "
            
        user_input = input(formatted_prompt).strip()
        
        if not user_input and default:
            return default
        if user_input:
            return user_input
        if not required and not user_input:
            return ""
            
        print_error("This field is required. Please enter a value.")

def main():
    clear_screen()
    
    print_header("Photofolio: Interactive Setup Wizard")
    print_info("Welcome! This wizard will configure your Google Drive-powered portfolio.")
    print_info("Before starting, ensure you have completed Part 1 & 2 of the setup guide")
    print_info("to create a Google Service Account and organize your Google Drive.")
    print("")
    
    # Check if config.example.json exists
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example_config_path = os.path.join(base_dir, 'config.example.json')
    config_path = os.path.join(base_dir, 'config.json')
    
    if not os.path.exists(example_config_path):
        print_error(f"Could not find template file: {example_config_path}")
        print_info("Please ensure you are running this script from the project's root or scripts directory.")
        sys.exit(1)

    # ---------------------------------------------------------
    # STEP 1: Personal Details
    # ---------------------------------------------------------
    print_step("Step 1: Personal Details")
    print_info("These details will appear on your website header and sidebar.")
    
    name = get_input("Your Full Name (e.g., Jane Doe)")
    
    # Strip @ if user includes it unintentionally, we enforce it in UI or they can add it.
    handle = get_input("Your Display Handle (e.g., @janedoe)")
    if not handle.startswith('@'):
        handle = f"@{handle}"
        
    insta_url = get_input("Your Instagram URL (e.g., https://instagram.com/janedoe)")
    
    print_success("Personal details saved.")
    print("")

    # ---------------------------------------------------------
    # STEP 2: Google Drive Details
    # ---------------------------------------------------------
    print_step("Step 2: Google Drive Configuration")
    print_info("1. Open your 'Portfolio' folder in Google Drive in your web browser.")
    print_info("2. Look at the URL. It will look like: drive.google.com/drive/folders/YOUR_ID_HERE")
    print_info("3. Copy that long string of characters at the end.")
    print("")
    folder_id = get_input("Enter your Google Drive Folder ID")
    print_success("Google Drive folder connected.")
    print("")

    # ---------------------------------------------------------
    # STEP 3: Service Account Credentials
    # ---------------------------------------------------------
    print_step("Step 3: Authentication Credentials")
    print_info("To automatically pull your photos, the script needs your 'credentials.json' file.")
    print_info("This is the file you downloaded from the Google Cloud Console.")
    print("")
    
    credentials_dest = os.path.join(base_dir, 'credentials.json')
    
    if os.path.exists(credentials_dest):
        print_success(f"✓ Found existing credentials.json in the project root.")
        update_creds = get_input("Do you want to replace it? (y/N)", default="N", required=False).lower()
        if update_creds != 'y':
            print_info("Skipping credentials update.")
        else:
            handle_credentials_upload(base_dir, credentials_dest)
    else:
        handle_credentials_upload(base_dir, credentials_dest)

    # ---------------------------------------------------------
    # STEP 4: Generate Config
    # ---------------------------------------------------------
    print_step("Step 4: Finalizing Configuration")
    print_info("Creating your local config.json file...")
    
    # Read template structure just to be safe, though we can construct dict directly
    with open(example_config_path, 'r') as f:
        config_data = json.load(f)
        
    config_data['name'] = name
    config_data['handle'] = handle
    config_data['instagram_url'] = insta_url
    config_data['google_drive_folder_id'] = folder_id
    
    # Write new config
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)
        
    print_success(f"Configuration saved to {config_path}")
    print_warning("Note: config.json is intentionally ignored by source control (Git) to protect your secrets.")
    
    print_header("Setup Complete! 🎉")
    print_info("You are now ready to build and view your portfolio.")
    print_info("Run the following command to download your photos and generate the site:")
    print(f"\n{Colors.GREEN}{Colors.BOLD}    ./deploy.sh{Colors.ENDC}\n")


def handle_credentials_upload(base_dir, dest_path):
    while True:
        creds_path = get_input("Enter the absolute path to your downloaded credentials.json file (e.g., /Users/name/Downloads/project-key.json)")
        
        # Expand ~ if used
        creds_path = os.path.expanduser(creds_path)
        
        if not os.path.exists(creds_path):
            print_error(f"File not found: {creds_path}")
            continue
            
        if not creds_path.endswith('.json'):
            print_error("The file must be a JSON file.")
            continue
            
        try:
            # Try to parse it to ensure it's valid JSON
            with open(creds_path, 'r') as f:
                json_data = json.load(f)
                
            if "client_email" not in json_data or "private_key" not in json_data:
                print_warning("The file doesn't look like a standard Google Service Account key.")
                confirm = get_input("Are you sure this is the correct file? (y/n)", default="n").lower()
                if confirm != 'y':
                    continue
                    
            shutil.copy2(creds_path, dest_path)
            print_success(f"Credentials successfully securely copied to the project.")
            break
            
        except json.JSONDecodeError:
            print_error("The file is not a valid JSON document.")
        except Exception as e:
            print_error(f"Failed to copy file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup wizard cancelled by user.{Colors.ENDC}")
        sys.exit(0)
