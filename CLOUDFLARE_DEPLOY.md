# Cloudflare Pages Deployment Guide

Complete guide to deploying your photography portfolio to Cloudflare Pages.

## Why Cloudflare Pages?

| Feature | Cloudflare Pages | GitHub Pages |
|---------|------------------|--------------|
| **Bandwidth** | Unlimited | Soft limit ~100GB/month |
| **Build time** | 500 builds/month free | Unlimited |
| **Custom domains** | Unlimited | 1 per repo |
| **Global CDN** | ✅ 200+ cities | ✅ Limited |
| **Image handling** | Better | Basic |
| **Speed** | Faster | Good |

**Verdict**: Cloudflare Pages is better for image-heavy portfolios!

## Prerequisites

- GitHub account
- Cloudflare account (free - sign up at https://cloudflare.com)
- Your portfolio code in a GitHub repository

## Step-by-Step Setup

### 1. Push Your Code to GitHub

If you haven't already:

```bash
cd /Users/prathampunj/Desktop/Weekend\ Projects/portfolio_struct

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial portfolio setup"

# Create GitHub repo first (at github.com/new), then:
git remote add origin https://github.com/Sensibleprat/photo_portfolio.git
git branch -M main
git push -u origin main
```

### 2. Connect Cloudflare Pages

1. **Go to Cloudflare Dashboard**
   - Visit: https://dash.cloudflare.com
   - Login or create free account

2. **Navigate to Pages**
   - Click "Workers & Pages" in sidebar
   - Click "Create application"
   - Select "Pages" tab
   - Click "Connect to Git"

3. **Connect GitHub**
   - Click "Connect GitHub"
   - Authorize Cloudflare
   - Select your repository: `photo_portfolio`

4. **Configure Build Settings**
   
   **Important**: Use these exact settings:
   
   - **Project name**: `photo-portfolio` (or your choice)
   - **Production branch**: `main`
   - **Framework preset**: None
   - **Build command**: (leave empty)
   - **Build output directory**: `site`
   - **Root directory**: (leave empty)

5. **Environment Variables**
   - None needed for static sites

6. **Save and Deploy**
   - Click "Save and Deploy"
   - Wait ~30 seconds for first deployment

### 3. Access Your Site

After deployment completes:

- **Cloudflare URL**: `https://photo-portfolio-xyz.pages.dev`
- Copy this URL to share with others!

### 4. Custom Domain (Optional)

Want your own domain like `photos.yourname.com`?

1. **In Cloudflare Pages**:
   - Go to your project → "Custom domains"
   - Click "Set up a custom domain"
   - Enter your domain

2. **DNS Configuration**:
   - Add a CNAME record pointing to your Pages URL
   - Cloudflare handles SSL automatically!

## Workflow After Setup

### Every Time You Update Photos:

1. **Add photos to Google Drive** (in your organized folders)

2. **Run deployment script**:
   ```bash
   cd /Users/prathampunj/Desktop/Weekend\ Projects/portfolio_struct
   source .venv/bin/activate
   ./deploy.sh
   ```

3. **Automatic deployment**:
   - Script syncs from Drive → Local
   - Processes images
   - Generates site
   - Pushes to GitHub
   - Cloudflare auto-deploys (30 seconds)
   - Your site is updated! ✨

### Manual Deployment (if needed):

```bash
# Sync photos
python sync_from_drive.py

# Process images
python optimize_images.py

# Generate site
python generate_site.py

# Deploy
git add .
git commit -m "Update photos"
git push origin main
```

Cloudflare detects the push and auto-deploys.

## Monitoring Deployments

View deploy status:
1. Go to Cloudflare Dashboard → Pages
2. Click your project
3. See deployment history

Each deployment shows:
- Build logs
- Deploy time
- Status (success/failed)
- Preview URL

## Troubleshooting

### Build Fails

**Issue**: Cloudflare build fails

**Solution**: 
- Make sure build command is EMPTY
- Build output directory is `site`
- The `site/` folder exists in your repo

### Site Shows 404

**Issue**: Gets 404 error

**Solution**:
- Check `site/index.html` exists
- Verify build output directory is `site`
- Check deployment logs for errors

### Images Not Loading

**Issue**: HTML loads but images missing

**Solution**:
- Run `python generate_site.py` locally first
- Check `site/data.json` has correct paths
- Verify `optimized/` folder has images
- Check relative paths in `data.json`

### Push Rejected

**Issue**: `git push` fails

**Solution**:
```bash
git pull origin main --rebase
git push origin main
```

## Advanced: Preview Deployments

Cloudflare creates preview URLs for every branch/PR:

```bash
# Create a feature branch
git checkout -b new-photos
# Make changes
git add .
git commit -m "Add new photos"
git push origin new-photos
```

Cloudflare automatically deploys to a preview URL like:
`https://abc123.photo-portfolio.pages.dev`

## Performance Optimization

### Enable Compression

In Cloudflare Dashboard:
- Speed → Optimization
- Enable Auto Minify (HTML, CSS, JS)

### Image Optimization

Cloudflare can further optimize images:
- Speed → Optimization  
- Enable "Polish" (requires paid plan)

Or keep using our script with `ENABLE_OPTIMIZATION = True`

## Rollback Deployments

Made a mistake? Rollback easily:

1. Go to Cloudflare Pages → Your Project
2. Click "View build" on a previous deployment
3. Click "Rollback to this deployment"
4. Confirm

Your site reverts to the previous version instantly!

## Cost

**Free tier includes:**
- Unlimited requests
- Unlimited bandwidth
- 500 builds/month
- Global CDN

**You'll never need to pay** for a photography portfolio!

## Summary

✅ **Setup once** - Connect GitHub to Cloudflare  
✅ **Update anytime** - Just run `./deploy.sh`  
✅ **Auto-deploy** - Cloudflare handles the rest  
✅ **Free forever** - No hidden costs  

---

Your portfolio is now live with enterprise-grade hosting - for free! 🚀
