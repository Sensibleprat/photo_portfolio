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

# Step# 2. Sync from Drive (Optional - uncomment if needed)
# echo "🔄 Syncing from Google Drive..."
# python scripts/sync_from_drive.py

# 3. Optimize Images
echo "🖼️  Optimizing images..."
python scripts/optimize_images.py

# 4. Generate Site
echo "🏗️  Building site..."
python scripts/generate_site.py
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
