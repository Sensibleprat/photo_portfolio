# Photography Portfolio

A minimal, high-performance photography portfolio website that syncs dynamically from **Google Drive** and hosts on **Cloudflare Pages**.

## ✨ Features
-   **Google Drive Sync**: Manage your photos in Drive; they appear on your site.
-   **Auto-Optimization**: Automatically converts HEIC to JPG and optimizes for web.
-   **Folder-based Organization**: Simply create folders in Drive (e.g., "Nature", "Urban") to create tabs.
-   **Blazing Fast**: Static site generation + 12-item pagination ("Load More") ensures instant loading.
-   **Smart Randomization**: The "All Photos" tab is shuffled at build-time to show a fresh mix of your work.
-   **Deep Linking**: Click any photo to see the full-quality original in Drive.

## 🚀 Getting Started

Please see the [Setup Guide](docs/setup.md) for complete instructions.

## 📂 Documentation

-   [Setup Guide](docs/setup.md): Step-by-step installation and configuration.
-   [Architecture & History](docs/architecture_history.md): How it works and design decisions.

## 🛠 Quick Update

If you have added new photos to Google Drive:

```bash
./deploy.sh
```

This command will:
1. **Sync** new photos from Google Drive.
2. **Optimize** them for the web.
3. **Generate** the site.
4. **Deploy** to Cloudflare Pages.

---
*Created by [Sensibleprat](https://github.com/Sensibleprat)*
