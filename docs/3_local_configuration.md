# Part 3: Local Configuration & Build

Now that your Google Drive is prepped and your Service Account is created, we need to bridge the gap between "the cloud" and "the code". By configuring the scripts locally, we establish the bridge that downloads, optimizes, and structures your portfolio.

## Step 1: Download the Code
You don't need to know how to use Git. Simply go to the repository page on GitHub, click the green **Code** button, and select **Download ZIP**.

Extract the ZIP file, open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux), and navigate into the extracted folder.

## Step 2: Set Up Python
The build scripts require Python. If you don't already have it installed, run the corresponding command for your system:

**Mac**:
```bash
brew install python3
```

**Ubuntu/Debian Linux**:
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip -y
```

**Windows**:
Download and run the installer from [python.org](https://www.python.org/downloads/). **Make sure to check the box that says "Add Python to PATH" during installation.**

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
python3 scripts/setup_wizard.py
```

The wizard will ask for:
1. Your Name, Handle, and Instagram URL.
2. Your Google Drive Folder ID (from Part 2).
3. The location of your `credentials.json` file (from Part 1), which it will securely copy into the project for you.

*(Note: You can also manually add `"profile_picture": "your_image.jpg"` to your `config.json` after setup, and place that image inside your local `photos/` directory to have it appear on the homepage!)*

## Step 4: Test the Build Locally
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
