# Part 4: Deployment & CI/CD (Cloudflare Pages)

We have built a high-performance, statically generated portfolio. To host it globally for free, we will use **Cloudflare Pages**. 

> [!NOTE]
> **Architect's Insight: How the CI/CD Pipeline Works**
> Cloudflare Pages usually pulls source code and runs build commands itself. However, because our build requires a secure `credentials.json` file to talk to Google Drive, it's safer and less complex to **build the site locally** and push the finished product (`site/`) to GitHub. Cloudflare will simply serve the `site/` directory whenever you push.

## Step 1: Push Your Project to GitHub
First, you need to store your version of this repository on your own GitHub account.

1. Create a **New Repository** on your GitHub account (e.g., `my-portfolio`).
2. Make it **Public** (required for Cloudflare free tier to attach easily, though private works if you authorize the app).
3. Connect your local folder to your new repository and push:

```bash
# If you cloned from the original template, you'll need to update the origin URL:
git remote set-url origin https://github.com/YOUR_USERNAME/my-portfolio.git

# Push your changes (including the generated site/ folder):
git branch -M main
git push -u origin main
```

*(Note: The `./deploy.sh` script automatically runs `git add .`, `git commit`, and `git push` for subsequent updates)*.

## Step 2: Set Up Cloudflare Pages
1. Create a free account at [Cloudflare](https://dash.cloudflare.com/sign-up).
2. Go to **Workers & Pages** in the left sidebar.
3. Click **Create Application**.
4. Select the **Pages** tab and click **Connect to Git**.
5. Connect your GitHub account and select your `my-portfolio` repository.

## Step 3: Configure Build Settings
During setup, Cloudflare will ask how to build your site. Since we already built it locally using `./deploy.sh`, we just want Cloudflare to host the `site/` folder.

Fill out the form exactly like this:
- **Framework Preset**: `None`
- **Build Command**: `exit 0`
- **Build Output Directory**: `site`

Click **Save and Deploy**.

## Step 4: The Final Workflow
Your portfolio is live! 🚀 Cloudflare will give you a free `<something>.pages.dev` URL.

### How to update your website in the future:
1. Add or remove photos in your Google Drive folders.
2. Open your terminal in your project directory.
3. Run:
   ```bash
   ./deploy.sh
   ```
4. **Done.** The script will sync the changes (downloading new photos and removing deleted ones), resize them, update the HTML, commit the changes to your local Git, and push them to GitHub. Cloudflare will detect the push and automatically update your live site within seconds!

> [!SUCCESS]
> **Congratulations!** You have successfully orchestrated a modern, free, automated Google-Drive-to-Website pipeline.
