# 📸 Photography Portfolio - Static Site Generator

A beautiful, fast, and completely free photography portfolio website that auto-generates from your local photo folders. No servers, no API limits, just pure static hosting magic.

## 🌟 Features

- ✅ **Zero Cost** - Host on GitHub Pages for free
- ✅ **No Server Required** - Pure static site
- ✅ **Auto-Organization** - Folder names become navigation tabs
- ✅ **One-Command Deployment** - Update your portfolio in seconds
- ✅ **Fast & Reliable** - No rate limits or API quotas
- ✅ **Image Optimization** - Automatic compression and resizing
- ✅ **Responsive Design** - Beautiful on all devices

## 📁 Project Structure

```
portfolio_struct/
├── photos/                    # Your photo folders
│   ├── Nature/               # Each folder = 1 tab on website
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   ├── Street/
│   └── Landscape/
├── optimized/                # Auto-generated optimized images
├── site/                     # Generated website files
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── data.json
├── generate_site.py          # Main site generator
├── optimize_images.py        # Image optimization script
├── deploy.sh                 # One-click deployment
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Git
- GitHub account (for hosting)

### Installation

1. **Clone or download this repository**
   ```bash
   cd portfolio_struct
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your photos**
   - Create folders inside `photos/` directory
   - Each folder name becomes a tab (e.g., `Nature`, `Street`, `Portraits`)
   - Add your photos to these folders

4. **Generate your portfolio**
   ```bash
   python generate_site.py
   ```

5. **Test locally**
   ```bash
   # Open site/index.html in your browser
   # OR run a local server:
   python -m http.server 8000 --directory site
   # Visit: http://localhost:8000
   ```

## 📤 Deployment to GitHub Pages

### First-Time Setup

1. **Create a new GitHub repository** (e.g., `my-portfolio`)

2. **Initialize Git in your project**
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio setup"
   ```

3. **Connect to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/my-portfolio.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages**
   - Go to your repo → Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` → `/site` folder
   - Save

5. **Your site will be live at:**
   ```
   https://YOUR_USERNAME.github.io/my-portfolio/
   ```

### Updating Your Portfolio (Every Time)

Just run this one command:

```bash
./deploy.sh
```

This script will:
1. Optimize your images
2. Generate the website
3. Commit changes
4. Push to GitHub
5. Your site updates automatically! 🎉

## 🎨 Customization

### Change Site Title & Author

Edit `site/index.html`:
```html
<title>Your Name's Portfolio</title>
<h3>Your Name</h3>
<p>@YourHandle</p>
```

### Modify Styles

Edit `site/style.css` to customize colors, fonts, layout, etc.

### Add Profile Picture

Replace the `.profile-image` background in `site/style.css`:
```css
.profile-image {
    background-image: url('your-photo.jpg');
}
```

## 🔧 How It Works

1. **`generate_site.py`** - Scans `photos/` folder structure and creates `data.json`
2. **`optimize_images.py`** - Compresses and resizes images for web
3. **`index.html` + `script.js`** - Reads `data.json` and renders gallery dynamically
4. **GitHub Pages** - Serves your static site for free

## 📝 Image Optimization

The `optimize_images.py` script:
- Resizes large images to max 2000px (configurable)
- Compresses JPEGs to 85% quality
- Creates web-optimized versions
- Preserves originals in `photos/`

To adjust settings, edit the script variables:
```python
MAX_WIDTH = 2000
MAX_HEIGHT = 2000
JPEG_QUALITY = 85
```

## 🐛 Troubleshooting

**Images not showing?**
- Check that image files are in supported formats (jpg, png, heic, etc.)
- Run `python generate_site.py` again
- Check browser console for errors

**Site not updating on GitHub?**
- Verify GitHub Pages is enabled in repo settings
- Check that you're pushing to the correct branch
- GitHub Pages can take 1-2 minutes to rebuild

**Script errors?**
- Ensure Python 3.7+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

## 📜 License

Free to use and modify for personal or commercial projects.

## 🤝 Contributing

This is a personal portfolio template, but feel free to fork and enhance it!

---

**Built with ❤️ for photographers who hate manual website updates**
