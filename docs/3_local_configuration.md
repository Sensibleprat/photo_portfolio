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

## Step 3: Run the Setup Wizard
Instead of manually configuring files and moving credentials around, simply run the interactive setup wizard. It will guide you through connecting your Google Drive and setting up your profile details.

```bash
python scripts/setup_wizard.py
```

The wizard will ask for:
1. Your Name, Handle, and Instagram URL.
2. Your Google Drive Folder ID (from Part 2).
3. The location of your `credentials.json` file (from Part 1), which it will securely copy into the project for you.

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
