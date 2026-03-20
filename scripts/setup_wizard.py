#!/usr/bin/env python3
import os
import json
import shutil
import sys
import webbrowser
import glob
from pathlib import Path
import urllib.request
import urllib.error

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
    print(f"\n{Colors.BLUE}{Colors.BOLD}➜ {text}{Colors.ENDC}")

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

def pause_for_user(prompt="Press Enter when you have completed this step..."):
    input(f"\n{Colors.WARNING}{Colors.BOLD}➤ {prompt}{Colors.ENDC}")

def auto_detect_credentials():
    print_info("Scanning your Downloads folder for Google Service Account keys...")
    downloads_dir = os.path.join(str(Path.home()), 'Downloads')
    
    # Get all JSON files in Downloads, sorted by newest first
    json_files = glob.glob(os.path.join(downloads_dir, '*.json'))
    json_files.sort(key=os.path.getmtime, reverse=True)
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Check if it looks like a Google Service Account key
                if "type" in data and data["type"] == "service_account" and "project_id" in data:
                    print_success(f"Found a potential Google Credentials file!")
                    filename = os.path.basename(file_path)
                    print_info(f"File: {filename}")
                    print_info(f"Project ID: {data.get('project_id')}")
                    
                    confirm = get_input("Is this the correct credentials file you just downloaded? (Y/n)", default="Y").lower()
                    if confirm == 'y':
                        return file_path
        except Exception:
            pass # Ignore files that aren't valid JSON or can't be read
            
    print_warning("Could not automatically find a valid Google credentials file in your Downloads folder.")
    return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Photofolio Setup Wizard")
    parser.add_argument("--skip-to-cloud", action="store_true", help="Skip Google Drive setup and go straight to GitHub/Cloudflare")
    args = parser.parse_args()

    clear_screen()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example_config_path = os.path.join(base_dir, 'config.example.json')
    config_path = os.path.join(base_dir, 'config.json')
    name = "Photofolio User"
    
    # Try to load existing name if config exists
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                name = json.load(f).get('name', "Photofolio User")
        except: pass

    if not args.skip_to_cloud:
        print_header("Photofolio: Interactive Setup Wizard")
        print_info("Welcome! I'll guide you step-by-step through setting up your photography portfolio.")
        print_info("No coding or technical experience required.")
        print("")
        print_warning("IMPORTANT: Before we begin, your Google Drive MUST be organized.")
        print_info("1. Create one main 'Portfolio' folder in your Drive.")
        print_info("2. Inside it, create sub-folders for each category (e.g., 'Nature', 'Street').")
        print_info("3. Place your photos exactly inside those sub-folders.")
        print("")
        pause_for_user("Press Enter when your Google Drive is organized and ready to go")
        
        # ---------------------------------------------------------
        # STEP 1: Personal Details
        # ---------------------------------------------------------
        clear_screen()
        print_step("Step 1: Your Profile")
        print_info("Let's set up the name and social links that will appear on your website.")
        print("")
        
        name = get_input("Your Full Name (e.g., Jane Doe)")
        
        handle = get_input("Your Display Handle (e.g., @janedoe)")
        if not handle.startswith('@'):
            handle = f"@{handle}"
            
        insta_url = get_input("Your Instagram URL (e.g., https://instagram.com/janedoe)")
        
        print_success("Profile details saved.")
        
        # ---------------------------------------------------------
        # STEP 2: Google Drive
        # ---------------------------------------------------------
    clear_screen()
    print_step("Step 2: Connect Google Drive")
    print_info("Your website uses Google Drive to store images. Think of it as your admin panel.")
    print_info("We need to create a folder for your portfolio and get its ID.")
    print("")
    
    open_drive = get_input("Press Enter to open Google Drive in your browser", required=False)
    webbrowser.open("https://drive.google.com/")
    
    print_info("\n1. Create a new folder in Google Drive (e.g., 'My Portfolio').")
    print_info("2. Double-click to open that new folder.")
    print_info("3. Look at the URL in your browser's top address bar.")
    print_info("   It will look like: drive.google.com/drive/folders/1KtAZreDObn...-")
    print_info("4. Copy that long string of characters at the very end after `.../folder/`.")
    print("")
    
    folder_id = get_input("Paste your Google Drive Folder ID here")
    print_success("Google Drive folder connected!")

    # ---------------------------------------------------------
    # STEP 3: Google Cloud (Service Account)
    # ---------------------------------------------------------
    clear_screen()
    print_step("Step 3: Creating a 'Bot User' (Service Account)")
    print_info("To allow your website to automatically download your photos without asking")
    print_info("you to log in every time, we need to create a Google Cloud 'Service Account'.")
    print("")
    
    pause_for_user("Press Enter to open the Google Cloud Console")
    webbrowser.open("https://console.cloud.google.com/projectcreate")
    
    print_info("\n1. You should now see a 'New Project' screen. Name it 'Portfolio' and click Create.")
    pause_for_user("Press Enter after your project finishes creating")
    
    print_info("\n2. Now we need to explicitly enable Google Drive access for this project.")
    pause_for_user("Press Enter to open the Drive API page")
    webbrowser.open("https://console.cloud.google.com/apis/library/drive.googleapis.com")
    
    print_info("\n3. Click the blue 'Enable' button on that page.")
    pause_for_user("Press Enter after enabling the API")
    
    print_info("\n4. Finally, let's create the actual 'Bot User' and download its password key.")
    pause_for_user("Press Enter to open the Service Accounts page")
    webbrowser.open("https://console.cloud.google.com/iam-admin/serviceaccounts/create")
    
    print_info("\n5. Give it a name (e.g., 'portfolio-bot') and click 'Create and Continue', then 'Done'.")
    print_info("6. On the next screen, click the Email address of the bot you just created.")
    print_info("7. Go to the 'KEYS' tab at the top.")
    print_info("8. Click 'Add Key' -> 'Create new key' -> Choose 'JSON' -> 'Create'.")
    print_warning("\nA file will automatically download to your computer. That is your secret key!")
    pause_for_user("Press Enter ONLY AFTER the file has downloaded")

    # ---------------------------------------------------------
    # STEP 4: Credential Collection & Sharing
    # ---------------------------------------------------------
    clear_screen()
    print_step("Step 4: Linking the Key")
    credentials_dest = os.path.join(base_dir, 'credentials.json')
    
    # Try Auto-Detect
    creds_path = auto_detect_credentials()
    
    if creds_path:
        shutil.copy2(creds_path, credentials_dest)
        print_success("Credentials successfully linked and safely copied to your project!")
    else:
        # Fallback to manual path
        print_info("Since we couldn't find the file automatically, please provide its path.")
        handle_credentials_upload(base_dir, credentials_dest)
        creds_path = credentials_dest

    # Extract the email address so the user can easily share the Drive folder
    try:
        with open(credentials_dest, 'r') as f:
            bot_email = json.load(f).get('client_email', 'ERROR-COULD-NOT-FIND-EMAIL')
            
        print_header("CRITICAL FINAL STEP: Folder Sharing")
        print_warning("The bot user MUST be invited to your Google Drive folder, or it cannot see your photos.")
        print("")
        print_info(f"1. Copy this exact email address: {Colors.BOLD}{Colors.WARNING}{bot_email}{Colors.ENDC}")
        print_info("2. Go back to your Google Drive folder.")
        print_info("3. Right-click the folder and click 'Share'.")
        print_info("4. Paste the email address, uncheck 'Notify people', and click 'Share'.")
        print("")
        pause_for_user("Press Enter when you have successfully shared the folder")
        
    except Exception as e:
        print_error(f"Could not read the service email to provide sharing instructions. Error: {e}")

    # ---------------------------------------------------------
    # STEP 5: Generate Config
    # ---------------------------------------------------------
    clear_screen()
    print_step("Step 5: Finalizing Local Setup")
    
    with open(example_config_path, 'r') as f:
        config_data = json.load(f)
        
    config_data['name'] = name
    config_data['handle'] = handle
    config_data['instagram_url'] = insta_url
    config_data['google_drive_folder_id'] = folder_id
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)
        
    print_success(f"Site configuration successfully saved!")

    # ---------------------------------------------------------
    # STEP 6: GitHub Code Storage (Invisible Git)
    # ---------------------------------------------------------
    clear_screen()
    print_step("Step 6: Creating Your Cloud Storage (GitHub)")
    print_info("To put your website on the internet, the code needs a home.")
    print_info("We will use GitHub to store your site for free.")
    print("")
    
    pause_for_user("Press Enter to open GitHub and generate an Access Token")
    # This URL pre-fills a token with exactly the right permissions
    webbrowser.open("https://github.com/settings/tokens/new?scopes=repo&description=Photofolio+Deployment")
    
    print_info("\n1. Scroll all the way to the bottom of the webpage and click the green 'Generate token' button.")
    print_info("2. Copy the green string of characters that appears (it starts with literally 'ghp_').")
    print("")
    
    github_token = get_input("Paste your GitHub Access Token here")
    
    # Use API to get username
    username = None
    try:
        req = urllib.request.Request("https://api.github.com/user", headers={"Authorization": f"token {github_token}"})
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
            username = user_data.get('login')
            print_success(f"Authenticated as GitHub user: {username}")
    except Exception as e:
        print_error(f"Failed to authenticate with GitHub. Are you sure you copied the token correctly? Error: {str(e)}")
        sys.exit(1)

    repo_name = get_input("\nWhat do you want to name your website's code repository online?", default="photo-portfolio")
    # Clean up the name for GitHub compatibility
    repo_name = repo_name.replace(" ", "-").lower()
    
    print_info(f"\nCreating a new cloud repository named '{repo_name}' for you...")
    try:
        # Create repo via API
        repo_data = json.dumps({"name": repo_name, "private": False}).encode('utf-8')
        req = urllib.request.Request("https://api.github.com/user/repos", data=repo_data, headers={"Authorization": f"token {github_token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            print_success("Cloud repository created successfully!")
    except urllib.error.HTTPError as e:
        if e.code == 422: # Unprocessable Entity (usually means repo already exists)
            print_warning("Repository already exists. We will link to the existing one.")
        else:
            print_error(f"Failed to create repository: {e.read().decode()}")
            sys.exit(1)
    except Exception as e:
        print_error(f"Failed to create repository: {str(e)}")
        sys.exit(1)

    print_info("\nLinking your computer to the cloud and uploading the latest code...")
    # Run the invisible git commands!
    os.chdir(base_dir)
    
    # Initialize Git if they downloaded via ZIP instead of git clone
    if not os.path.exists('.git'):
        os.system("git init > /dev/null 2>&1")
        os.system("git checkout -b main > /dev/null 2>&1")
        # Ensure credentials.json and config.json are ignored if .gitignore is missing or broken
        os.system("echo 'credentials.json' >> .gitignore")
        os.system("echo 'config.json' >> .gitignore")
        
    # Check if the user has a global git identity, otherwise commits will fail
    global_name = os.popen("git config --global user.name").read().strip()
    global_email = os.popen("git config --global user.email").read().strip()
    
    if not global_name or not global_email:
        print_info("\nWe need to tell your computer who is uploading this code.")
        git_name = get_input("What is your Name for GitHub records?", default=username)
        git_email = get_input("What Email Address did you use to sign up for GitHub?")
        
        # Save globally so it permanently fixes their computer for future operations
        os.system(f"git config --global user.name \"{git_name}\" > /dev/null 2>&1")
        os.system(f"git config --global user.email \"{git_email}\" > /dev/null 2>&1")
        print_success("Git identity permanently saved to your computer.")
    
    # Use the token in the URL so they never get prompted for a password by git
    remote_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
    
    os.system("git remote remove origin > /dev/null 2>&1")
    os.system(f"git remote add origin {remote_url} > /dev/null 2>&1")
    os.system("git add . > /dev/null 2>&1")
    os.system("git commit -m \"Initial Photofolio Setup\" > /dev/null 2>&1")
    
    print_info("Uploading (this may take a moment)...")
    if os.system("git push -u origin main > /dev/null 2>&1") == 0:
        print_success("Code successfully uploaded to GitHub!")
    else:
        print_warning("Could not automatically push to GitHub. You may need to do it manually later.")

    # ---------------------------------------------------------
    # STEP 7: Cloudflare Hosting
    # ---------------------------------------------------------
    clear_screen()
    print_step("Step 7: Launching to the Internet (Cloudflare Pages)")
    print_info("The final step is connecting Cloudflare so your website is hosted for free.")
    print("")
    
    pause_for_user("Press Enter to open Cloudflare Pages")
    webbrowser.open("https://dash.cloudflare.com/?to=/:account/pages/new")
    
    print_info("\n1. Click 'Connect to Git' and choose your new GitHub repository.")
    print_info("2. " + Colors.WARNING + Colors.BOLD + "CRITICAL:" + Colors.ENDC + " When Cloudflare asks for Build Settings, enter exactly this:")
    print_info(f"   - Framework Preset:   {Colors.BOLD}None{Colors.ENDC}")
    print_info(f"   - Build Command:      {Colors.BOLD}exit 0{Colors.ENDC}")
    print_info(f"   - Output Directory:   {Colors.BOLD}site{Colors.ENDC}")
    print_info("3. Click 'Save and Deploy'.")
    print_info("Note: The very first deployment right now will 'fail' because you haven't uploaded")
    print_info("your photos yet. We will do that next!")
    print("")
    pause_for_user("Press Enter after setting up Cloudflare")
    
    # ---------------------------------------------------------
    # CONCLUSION
    # ---------------------------------------------------------
    clear_screen()
    print_header("Setup Complete! 🎉")
    print_info("You did it! Your entire automated pipeline is connected.")
    print_info("Whenever you want to build and update your website, just run:")
    print(f"\n{Colors.GREEN}{Colors.BOLD}    ./deploy.sh{Colors.ENDC}\n")
    print_info("Run that command right now to perform your very first upload!")


def handle_credentials_upload(base_dir, dest_path):
    while True:
        creds_path = get_input("Drag and drop your downlaoded JSON file here, or type its absolute path")
        creds_path = os.path.expanduser(creds_path).strip()
        
        # Remove terminal escape characters if dragged and dropped
        if creds_path.startswith("'") and creds_path.endswith("'"):
            creds_path = creds_path[1:-1]
            
        if not os.path.exists(creds_path):
            print_error(f"File not found: {creds_path}")
            continue
            
        if not creds_path.endswith('.json'):
            print_error("The file must be a JSON file.")
            continue
            
        try:
            with open(creds_path, 'r') as f:
                json_data = json.load(f)
                
            if "client_email" not in json_data or "private_key" not in json_data:
                print_warning("The file doesn't look like a standard Google Service Account key.")
                confirm = get_input("Are you sure this is the correct file? (y/n)", default="n").lower()
                if confirm != 'y':
                    continue
                    
            shutil.copy2(creds_path, dest_path)
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
