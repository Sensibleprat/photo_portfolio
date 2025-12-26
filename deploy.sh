#!/bin/bash
#
# One-Click Portfolio Deployment Script
# Workflow: Google Drive → Local → Optimize → Generate → Deploy
#

set -e  # Exit on error

echo "🚀 Portfolio Deployment Script"
echo "================================"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
    echo ""
fi

# Step 1: Sync from Google Drive
echo "📥 Step 1/5: Syncing photos from Google Drive..."
python3 sync_from_drive.py
echo ""

# Step 2: Process Images
echo "📸 Step 2/5: Processing images..."
python3 optimize_images.py
echo ""

# Step 3: Generate Site
echo "🏗️  Step 3/5: Generating website..."
python3 generate_site.py
echo ""

# Step 4: Git Add & Commit
echo "📝 Step 4/5: Committing changes..."
git add .

# Get current date for commit message
DATE=$(date +"%Y-%m-%d %H:%M")
COMMIT_MSG="Update portfolio - $DATE"

if git diff --cached --quiet; then
    echo "   ℹ️  No changes to commit"
else
    git commit -m "$COMMIT_MSG"
    echo "   ✓ Changes committed"
fi
echo ""

# Step 5: Push
echo "🌐 Step 5/5: Pushing to repository..."
git push origin main
echo ""

echo "================================"
echo "✨ Deployment Complete!"
echo ""
echo "Your portfolio will be live in ~1 minute at:"
echo "https://Sensibleprat.github.io/photo_portfolio/"
echo ""
echo "💡 Tip: For Cloudflare Pages, connect your GitHub repo at:"
echo "   https://dash.cloudflare.com/pages"
echo ""
