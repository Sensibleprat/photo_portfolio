# 🚀 Quick Start - Cloudflare Pages Portfolio

Get your full-quality photography portfolio live in 10 minutes!

## Step 1: Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure Google Drive

1. **Your Google Drive folder must be shared with the service account**
2. **Update folder ID** in `sync_from_drive.py`:
   ```python
   PARENT_FOLDER_ID = 'YOUR_FOLDER_ID_HERE'
   ```

How to find folder ID:
- Open your photo folder in Google Drive
- URL looks like: `https://drive.google.com/drive/folders/1KtAZreDO...`
- Copy the part after `/folders/`

## Step 3: Sync & Generate

```bash
# Download photos from Google Drive
python sync_from_drive.py

# Process images (full quality by default!)
python optimize_images.py

# Generate website
python generate_site.py

# Test locally
python -m http.server 8000 --directory site
# Visit: http://localhost:8000
```

## Step 4: Deploy to Cloudflare Pages

### First Time Setup:

```bash
# Initialize Git
git init

# Commit everything
git add .
git commit -m "Initial portfolio"

# Push to GitHub
git remote add origin https://github.com/Sensibleprat/photo_portfolio.git
git push -u origin main
```

### Connect Cloudflare Pages:

1. Go to https://dash.cloudflare.com/pages
2. Click "Create a project"
3. Connect GitHub account
4. Select `photo_portfolio` repository
5. **Build configuration:**
   - Build command: (leave empty)
   - Build output directory: `site`
6. Click "Save and Deploy"

🎉 Your site is live! Cloudflare gives you a URL like: `photo-portfolio-abc.pages.dev`

## Step 5: Future Updates

Every time you add photos to Google Drive:

```bash
./deploy.sh
```

That's it! One command:
1. Syncs from Google Drive
2. Processes images
3. Generates website
4. Pushes to GitHub
5. Cloudflare auto-deploys

## 🎨 Customize

**Change your name:**
Edit `index.html` lines 18-19

**Adjust image quality:**
Edit `optimize_images.py` line 16:
```python
ENABLE_OPTIMIZATION = False  # False = full quality (default)
ENABLE_OPTIMIZATION = True   # True = compress (95% quality)
```

## 📋 Folder Structure in Google Drive

```
Your Photos Folder (share this with service account)
├── Nature/
│   ├── photo1.jpg
│   └── photo2.jpg
├── Street/
│   ├── photo3.jpg
│   └── photo4.jpg
└── Portraits/
    └── photo5.jpg
```

Each folder becomes a tab on your website!

## 🐛 Common Issues

**"No module named 'googleapiclient'"**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Sync fails - "credentials.json not found"**
- Ensure `old_google_drive_version/credentials.json` exists
- This is your service account key from Google Cloud

**No photos downloaded**
- Check folder ID is correct
- Verify service account has access to the folder
  (Share the folder with the service account email)

## 💡 Pro Tips

1. **Full quality by default** - Your photos stay pristine!
2. **Your laptop doesn't need to be on** - Cloudflare hosts everything 24/7
3. **Updates are instant** - Just run `./deploy.sh`
4. **Unlimited bandwidth** - Cloudflare Pages is free with no bandwidth limits

---

**Need more details?** Check [README.md](README.md)
