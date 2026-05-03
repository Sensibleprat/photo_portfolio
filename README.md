# Photography Portfolio

A minimal, high-performance photography portfolio website that syncs dynamically from **Google Drive** and hosts on **Cloudflare Pages**.

**Live Demo:** [View an example portfolio built with this framework](https://photo-portfolio-17f.pages.dev/)

## ✨ Features
-   **Google Drive Sync**: Manage your photos in Drive; they appear on your site.
-   **Auto-Optimization**: Automatically converts HEIC to JPG and optimizes for web.
-   **Folder-based Organization**: Simply create folders in Drive (e.g., "Nature", "Urban") to create tabs.
-   **Blazing Fast**: Static site generation + 12-item pagination ("Load More") ensures instant loading.
-   **Smart Randomization**: The "All Photos" tab is shuffled at build-time to show a fresh mix of your work.
-   **Interactive Setup**: A guided terminal wizard makes configuring your site effortless.
-   **Deep Linking**: Click any photo to see the full-quality original in Drive.

## 🚀 Getting Started

> **⚠️ Prerequisite**: You must have Python installed.
> - **Mac**: `brew install python3`
> - **Ubuntu**: `sudo apt update && sudo apt install python3 python3-venv python3-pip -y`
> - **Windows**: [Download installer from python.org](https://www.python.org/downloads/)

To configure your own portfolio locally, simply download the repository code and run the built-in wizard:

1. Click the green **Code** button at the top of this repository and select **Download ZIP**.
2. Extract the ZIP file and open your terminal inside the extracted folder.
3. Run the following commands to install dependencies and start the wizard:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 scripts/setup_wizard.py
```

The wizard will interactively guide you through connecting your Google Drive and setting up your profile. For the full end-to-end guide on creating your Google Cloud bot and deploying to Cloudflare, see the **[Architect's Setup Guide](docs/setup.md)**.

## 📂 Documentation

-   [Setup Guide](docs/setup.md): Step-by-step installation and configuration.
-   [Architecture & History](docs/architecture_history.md): How it works and design decisions.

## 🛠 Quick Update

If you have added or removed photos in Google Drive:

```bash
./deploy.sh
```

This command will:
1. **Sync** photos from Google Drive (handling both new additions and removals).
2. **Optimize** them for the web.
3. **Generate** the site.
4. **Deploy** to Cloudflare Pages.

---
*Created by [Sensibleprat](https://github.com/Sensibleprat)*
