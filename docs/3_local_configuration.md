# Part 3: Local Configuration & Build

Now that your Google Drive is prepped and your Service Account is created, we need to bridge the gap between "the cloud" and "the code". By configuring the scripts locally, we establish the bridge that downloads, optimizes, and structures your portfolio.

## Step 1: Clone the Repository
Open a terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux) and clone this repository to your local machine:

```bash
git clone https://github.com/Sensibleprat/photo_portfolio.git
cd photo_portfolio
```

## Step 2: Set Up Python
The build scripts require Python. Setting up a "virtual environment" ensures these scripts don't conflict with other Python tools on your computer.

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
pip install -r requirements.txt
```

> [!TIP]
> **Architect's Insight: Dependencies** 
> The `requirements.txt` installs `Pillow` (for image resizing) and `pillow-heif` (for converting Apple's HEIC photo format to standard web-friendly JPGs). It also installs the Google API libraries needed to fetch your photos.

## Step 3: Add Credentials
Move the `credentials.json` file you downloaded in Part 1 to the root folder of this project (the folder containing `README.md`).

## Step 4: Configure `config.json`
The repository comes with a template configuration file named `config.example.json`. This file tells the build script your name, your Instagram, and which Google Drive folder holds your art.

1. **Copy the template**:
   ```bash
   cp config.example.json config.json
   ```
2. **Open `config.json` in a text editor**.
3. Fill it out with your specific details:

```json
{
    "name": "Your Awesome Name",
    "handle": "@yourhandle",
    "instagram_url": "https://www.instagram.com/yourhandle/",
    "profile_picture": "profile.png",
    "google_drive_folder_id": "THE_ID_YOU_COPIED_IN_PART_2"
}
```

> [!CAUTION]
> **Avoid Committing Secrets:** Like `credentials.json`, your `config.json` file contains unique identifiers. By default, the `.gitignore` prevents you from uploading this to GitHub, keeping your setup secure. The only file that goes to GitHub is `config.example.json`.

## Step 5: Test the Build Locally
Let's see the magic happen. Run the deployment script to trigger the full sync -> optimize -> build cycle:

```bash
./deploy.sh
```

**What is happening under the hood?**
1. **Sync**: `scripts/sync_from_drive.py` downloads your photos to a local `photos/` folder.
2. **Optimize**: `scripts/optimize_images.py` converts HEIC to JPG and resizes images into an `optimized/` folder.
3. **Generate**: `scripts/generate_site.py` combines your details, the images, and the HTML template into a final, deploy-ready `site/` folder.

If everything ran successfully without errors, your portfolio is correctly pulling from Drive!

## Next Steps
Your website exists entirely inside the `site/` directory on your computer. Now, we just need to push it to the internet so the world can see it.

➡️ Proceed to **[Part 4: Deployment & CI/CD](4_deployment_guide.md)**
