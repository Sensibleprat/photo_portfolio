# Portfolio Setup Guide

This guide will help you set up your own photography portfolio using Google Drive and Cloudflare Pages.

## 🛠 Prerequisites

-   **Python 3.8+** installed on your machine.
-   **Git** installed.
-   A **Google Cloud Platform** project (for Drive API).
-   A **Cloudflare** account (free tier is fine).
-   A **GitHub** account.

---

## 🚀 Step 1: Google Drive Setup

You need to enable the Drive API to allow the script to download your photos.

1.  **Create a Project** in [Google Cloud Console](https://console.cloud.google.com/).
2.  Enable the **Google Drive API**.
3.  Create a **Service Account**:
    -   Go to **IAM & Admin** > **Service Accounts**.
    -   Create a new service account.
    -   Create a new **Key** (JSON type).
    -   Download the JSON file and save it as `credentials.json` in the root of your project directory.
    -   *(Note: The script expects it at `./credentials.json`)*.
4.  **Organize Photos**:
    -   Create a main folder in Google Drive (e.g., "Portfolio").
    -   Inside it, create subfolders for your categories (e.g., "Nature", "Street", "Travel").
    -   Upload your photos to these subfolders.
5.  **Share Folder**:
    -   Open your "Portfolio" folder in Drive.
    -   Click **Share** and add the **Service Account Email** (found in your JSON file) as a **Viewer**. This gives the script permission to see the photos.
6.  **Get Folder ID**:
    -   Open the folder in your browser.
    -   Copy the ID from the URL: `drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE`.

---

## ⚙️ Step 2: Configuration

Open `config.json` in the project root and update it with your details:

```json
{
    "name": "Your Name",
    "handle": "@your_instagram_handle",
    "instagram_url": "https://www.instagram.com/<your_handle>/",
    "profile_picture": "profile.png",
    "google_drive_folder_id": "YOUR_FOLDER_ID_HERE"
}
```

*   **name**: Your full name (displayed in sidebar).
*   **handle**: Your social media handle text.
*   **instagram_url**: The full URL to your Instagram profile (required).
*   **profile_picture**: Place your profile image (e.g., `profile.png`) inside the `photos/` directory.
*   **google_drive_folder_id**: The ID you copied in Step 1.

> [!IMPORTANT]
> All fields are required. The build scripts will fail if any variable is missing.

---

## 💻 Step 3: Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/photo-portfolio.git
    cd photo-portfolio
    ```

2.  **Install Dependencies**:
    Recommended to use a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Sync Photos**:
    Run the sync script to grab photos and links from Drive:
    ```bash
    python sync_from_drive.py
    ```
    *(This creates `drive_links.json` which maps images to their Drive URLs)*.

4.  **Generate Site**:
    Process images (convert HEIC to JPG) and build the site:
    ```bash
    python optimize_images.py
    python generate_site.py
    ```

5.  **Preview**:
    ```bash
    python -m http.server 8000 --directory site
    ```
    Visit `http://localhost:8000`.

---

## ☁️ Step 4: Deployment (Cloudflare Pages)

1.  **Push to GitHub**:
    Commit your code (ensure `site/` folder is included, but `photos/` and `optimized/` are ignored).
    ```bash
    git add .
    git commit -m "Initial deploy"
    git push origin main
    ```

2.  **Cloudflare Pages**:
    -   Log in to **Cloudflare Dashboard**.
    -   Go to **Workers & Pages** > **Create Application** > **Pages** > **Connect to Git**.
    -   Select your **GitHub Repository**.
    -   **Build Settings**:
        -   **Framework Preset**: `None`
        -   **Build Command**: `exit 0` (Since we build locally and push the static site).
        -   **Output Directory**: `site`
    -   Click **Save and Deploy**.

🎉 **Done!** context: Your site will auto-deploy whenever you push to GitHub.

---

## 🔄 Updating Your Portfolio

1.  Add new photos to **Google Drive**.
2.  Run the update script:
    ```bash
    ./deploy.sh
    ```
    *(This script automates sync, generation, and git push)*.

---

## ⚠️ Important Notes

-   **Credentials**: NEVER commit `credentials.json` to GitHub. The `.gitignore` is set up to exclude it, but always double-check.
-   **HEIC Files**: The system automatically converts HEIC images to JPG for web compatibility.
