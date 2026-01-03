# Architecture & Development History

This document tracks the evolution of the project, including key decisions, changes, and migration steps.

## 🏗 Current Architecture (Cloudflare Pages + Google Drive)

*   **Source of Truth**: Google Drive (Stores original high-res photos).
*   **Build System**: Local Python scripts (`sync_from_drive.py`, `optimize_images.py`, `generate_site.py`).
*   **Hosting**: Cloudflare Pages (Serves static content from the `site/` directory).
*   **Version Control**: GitHub (Stores code + generated static assets).

### Workflow
1.  **Sync**: `scripts/sync_from_drive.py` downloads structure/images from Drive using Service Account.
2.  **Optimize**: `scripts/optimize_images.py` converts HEIC -> JPG (95% quality) and resizes if needed.
3.  **Generate**: `scripts/generate_site.py` builds `data.json`, copies assets, and injects config (Name, Handle).
4.  **Deploy**: Git Push triggers Cloudflare deployment.

---

## 📜 History of Changes

### Phase 1: Google Drive API (Frontend Only)
*   **Initial Approach**: The site used JavaScript to fetch images directly from Google Drive API on the client side.
*   **Problem**: Hit API rate limits immediately. Slow loading. Required exposing API keys (risky).

### Phase 2: Migration to Static Build (Current)
*   **Trigger**: Need for performance, reliability, and better SEO.
*   **Solution**: Moved image fetching to a "build step" (Python script).
*   **Key Decisions**:
    *   **Sync Script**: Downloads photos locally first. Solves rate limits since we only sync when developing.
    *   **Image Storage**: We do **not** commit the `photos/` (raw) or `optimized/` (processed) folders to GitHub to avoid repo size limits. We only commit the final `site/` folder. The `photos/` folder is now ephemeral—it is re-downloaded from Drive by `sync_from_drive.py` if missing.
    *   **Hosting Switch**: Switched to Cloudflare Pages for better performance and easier "Git-hook" deployments compared to manual FTP/hosting.

### Phase 3: HEIC Support & Customization
*   **Issue**: iPhone photos (HEIC) were not displaying in browsers.
*   **Fix**: Added `pillow-heif` to `optimize_images.py` to auto-convert HEIC to JPG.
*   **Refactor**: Extracted user details (Name, Handle, Drive ID) into `config.json` to make the project re-usable for others.
*   **Feature**: Added "Deep Linking" - clicking an image now opens the original Google Drive file (fetched via API metadata).

---

## 📂 File Structure Explanation

*   `docs/`: Documentation (You are here).
*   `src/`: Frontend source code (`index.html`, `style.css`, `script.js`).
*   `scripts/`: Python build tools (`sync_from_drive.py`, `optimize_images.py`, `generate_site.py`).
*   `site/`: The actual website (HTML/CSS/JS + processed images). This is what gets deployed.
*   `photos/`: Local cache of raw images from Drive (GitIgnored).
*   `optimized/`: Intermediate processed images (GitIgnored).
*   `config.json`: User settings (GitIgnored).
*   `config.example.json`: Template for user settings.
