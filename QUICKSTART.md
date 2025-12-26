# 🚀 Quick Start Guide

Get your portfolio up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Add Your Photos

Create category folders inside `photos/` directory:

```bash
mkdir -p photos/Nature photos/Street photos/Portraits
```

Copy your photos into these folders. Each folder will become a tab on your website!

## Step 3: Generate Your Site

```bash
# Optimize images for web
python optimize_images.py

# Generate website
python generate_site.py
```

## Step 4: Test Locally

```bash
# Start local server
python -m http.server 8000 --directory site

# Open in browser
open http://localhost:8000
```

## Step 5: Deploy to GitHub Pages

### First Time Setup:

```bash
# Initialize git
git init

# Create .gitignore
python generate_site.py  # This creates .gitignore automatically

# Make first commit
git add .
git commit -m "Initial portfolio setup"

# Create GitHub repo and connect
# (Create a new repo on GitHub first, then run:)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Enable GitHub Pages:
1. Go to your repo on GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` → `/site` folder
5. Save

Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO/`

## Future Updates (Every Time You Add Photos)

Just run:

```bash
./deploy.sh
```

That's it! One command to update everything! 🎉

## Customization

Edit these files to personalize:
- `index.html` - Change your name and handle
- `style.css` - Customize colors and design
- `generate_site.py` - Adjust image paths or settings

## Troubleshooting

**Script errors?**
```bash
python3 --version  # Check Python version (need 3.7+)
pip3 install -r requirements.txt  # Reinstall dependencies
```

**Images not showing?**
- Check that photos are in supported formats (jpg, png, heic)
- Run `python optimize_images.py` again
- Check browser console for errors

**Need help?**
Check the main [README.md](README.md) for detailed documentation.
