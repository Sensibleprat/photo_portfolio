# Photofolio: The Architect's Setup Guide

Welcome to Photofolio. This system is designed to provide you with a high-performance, ultra-fast photography portfolio with **zero maintenance**. 

As an engineer, you know that the best tools fade into the background. Instead of building a complex, custom Content Management System (CMS) with a database, authentication, and an admin dashboard, this architecture leverages the tools you already use daily: **Google Drive**.

## The Architecture at a Glance
1. **Source of Truth**: Google Drive. You manage your portfolio entirely by creating folders and dropping photos into them.
2. **Build Engine**: Local Python scripts download the photos, optimize them (converting massive iPhone HEIC files to web-friendly JPGs), and inject them into a static HTML template.
3. **Delivery**: GitHub stores the generated `site/` folder, and Cloudflare Pages serves it globally. The live site is simply static files, resulting in 100/100 Lighthouse performance scores and instant loading.

---

## 📚 The Setup Playbook

To set this up for your own portfolio, follow this 4-part guide sequentially. It looks like a lot, but you only have to do it once. After setup, updating your website is a single click.

### [Part 1: Google Cloud & Service Account Setup](1_google_cloud_setup.md)
*Create a "bot user" so your computer can talk to Google Drive securely without manual login prompts.*

### [Part 2: Google Drive Structure & Sharing](2_google_drive_setup.md)
*Organize your photos in Drive and explicitly share them with your new "bot user".*

### [Part 3: Local Configuration & Build](3_local_configuration.md)
*Clone this repository, configure your personal details, and run the magic `deploy.sh` script to pull your photos.*

### [Part 4: Deployment & CI/CD (Cloudflare Pages)](4_deployment_guide.md)
*Push your generated site to GitHub and connect Cloudflare Pages to host it globally for free.*

---

## 🛠 Quick Update (Post-Setup)

Once you have completed all four parts, adding new photos is trivially simple:

1. Drop new photos into your Google Drive folders.
2. Open your terminal in the project directory.
3. Run the master script:
   ```bash
   ./deploy.sh
   ```

*The script will automatically download the new photos, resize them, update the HTML, commit the changes to your local Git, and push them to GitHub. Cloudflare will detect the push and automatically update your live site within seconds!*
