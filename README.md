# 📸 Photography Portfolio - Google Drive + Cloudflare Pages

A beautiful, fast, and free photography portfolio that syncs from Google Drive and deploys to Cloudflare Pages. **Full quality images, no server required!**

## 🌟 Features

- ✅ **Zero Cost** - Free hosting on Cloudflare Pages
- ✅ **No Server Required** - Pure static site
- ✅ **Google Drive Integration** - Organize photos in Drive
- ✅ **Full Quality** - No compression by default
- ✅ **One-Command Deployment** - Sync, generate, and deploy instantly
- ✅ **Auto-Organization** - Folder names become navigation tabs
- ✅ **Responsive Design** - Beautiful on all devices

## 🏗️ Architecture

```
Google Drive (Storage)
      ↓ (sync on your laptop)
Local photos/ folder
      ↓ (optional optimization)
optimized/ folder
      ↓ (generate site)
site/ folder
      ↓ (deploy to Cloudflare)
Live Website (24/7 hosting)
```

**Your laptop only needed when updating!** After deployment, it can be off.

## 📁 Project Structure

```
portfolio_struct/
├── photos/                   # Downloaded from Google Drive
├── optimized/                # Processed images (git-ignored)
├── site/                     # Generated website
├── old_google_drive_version/ # Backup of original approach
│   └── credentials.json      # Google Drive service account
├── sync_from_drive.py        # Download photos from Drive
├── optimize_images.py        # Process images (optional compression)
├── generate_site.py          # Generate static site
├── deploy.sh                 # One-click deployment
├── index.html, style.css, script.js
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Git
- Google Drive with organized photos
- Google Cloud Service Account (for Drive API)

### Installation

1. **Install Dependencies**
   ```bash
   source .venv/bin/activate  # Activate virtual environment
   pip install -r requirements.txt
   ```

2. **Set Up Google Drive**
   - Your photos must be in a Google Drive folder
   - Each subfolder = 1 navigation tab (e.g., "Nature", "Street")
   - Service account credentials should be in `old_google_drive_version/credentials.json`
   - Update `PARENT_FOLDER_ID` in `sync_from_drive.py` with your folder ID

3. **Configure Image Quality**
   
   Edit [`optimize_images.py`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/optimize_images.py#L16):
   ```python
   ENABLE_OPTIMIZATION = False  # False = Full quality (default)
   JPEG_QUALITY = 95            # If optimization enabled, 95% quality
   ```

4. **First Sync & Generate**
   ```bash
   python sync_from_drive.py   # Download from Google Drive
   python optimize_images.py   # Process images
   python generate_site.py     # Generate website
   ```

5. **Test Locally**
   ```bash
   python -m http.server 8000 --directory site
   # Visit: http://localhost:8000
   ```

## 🌐 Deployment

### Option 1: Cloudflare Pages (Recommended)

**Why Cloudflare?**
- Free unlimited bandwidth
- Global CDN (faster than GitHub Pages)
- Better image handling
- Auto-deployment from GitHub

**Setup:**

1. **Push to GitHub** (first time)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/Sensibleprat/photo_portfolio.git
   git push -u origin main
   ```

2. **Connect to Cloudflare Pages**
   - Go to https://dash.cloudflare.com/pages
   - Click "Create a project"
   - Connect your GitHub repo
   - **Build settings:**
     - Build command: (leave empty)
     - Build output directory: `site`
   - Deploy!

3. **Future Updates**
   ```bash
   ./deploy.sh  # Syncs from Drive, generates site, pushes to GitHub
   # Cloudflare auto-deploys in ~30 seconds!
   ```

### Option 2: GitHub Pages

Follow the same GitHub setup, then:
- Go to repo Settings → Pages
- Source: Deploy from branch
- Branch: `main` → `/site` folder
- Save

Site live at: `https://Sensibleprat.github.io/photo_portfolio/`

## 🎨 Customization

### Change Your Name
Edit [`index.html`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/index.html#L18-L19):
```html
<h3>Your Name</h3>
<p>@YourHandle</p>
```

### Modify Styles
Edit [`style.css`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/style.css) for colors, fonts, layout.

### Enable Image Optimization
If you want to reduce file sizes:

Edit [`optimize_images.py`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/optimize_images.py#L16):
```python
ENABLE_OPTIMIZATION = True
JPEG_QUALITY = 95  # 95% quality (minimal loss)
MAX_WIDTH = 4000   # Max dimension
```

## 🔄 Workflow

### Adding New Photos

1. **Add to Google Drive** - Upload to your category folders
2. **Run deployment script:**
   ```bash
   ./deploy.sh
   ```
3. **Done!** Site updates automatically

That's it! One command does everything.

## ⚙️ Configuration

### Google Drive Folder ID

In [`sync_from_drive.py`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/sync_from_drive.py#L12):
```python
PARENT_FOLDER_ID = 'YOUR_FOLDER_ID_HERE'
```

To find your folder ID:
1. Open folder in Google Drive
2. URL: `https://drive.google.com/drive/folders/FOLDER_ID`
3. Copy the `FOLDER_ID` part

### Image Quality Settings

All in [`optimize_images.py`](file:///Users/prathampunj/Desktop/Weekend%20Projects/portfolio_struct/optimize_images.py#L11-L21):
- `ENABLE_OPTIMIZATION`: True/False
- `JPEG_QUALITY`: 1-100 (95 recommended if optimizing)
- `MAX_WIDTH/HEIGHT`: Max dimensions
- `PRESERVE_FORMAT`: Keep PNG as PNG, etc.

## 🐛 Troubleshooting

**"No module named 'PIL'" error?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Google Drive sync fails?**
- Check `credentials.json` exists in `old_google_drive_version/`
- Verify folder ID is correct
- Ensure service account has access to the folder

**Images not showing?**
- Run `python generate_site.py` again
- Check browser console for errors
- Verify `data.json` was created in `site/`

**Deployment fails?**
```bash
git remote -v  # Check remote is set
git remote add origin https://github.com/USERNAME/REPO.git
```

## 📊 Comparison: This vs Original

| Feature | Google Drive API | New Hybrid |
|---------|------------------|------------|
| **Storage** | Google Drive | Google Drive |
| **Hosting** | GitHub Pages | Cloudflare Pages |
| **Image Quality** | ❌ Compressed | ✅ Full quality |
| **Rate Limits** | ❌ Yes (500/day) | ✅ No |
| **Speed** | Slow | Fast (CDN) |
| **Workflow** | Complex | One command |
| **Laptop Always On?** | No | No |

## 📝 License

Free to use for personal or commercial projects.

---

**Built for photographers who want beautiful portfolios without compromising quality!** 📸
