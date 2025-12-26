#!/bin/bash
#
# One-Click Portfolio Deployment Script
# This script automates the entire workflow:
# 1. Optimizes images
# 2. Generates website
# 3. Commits changes
# 4. Pushes to GitHub
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

# Step 1: Optimize Images
echo "📸 Step 1/4: Optimizing images..."
python3 optimize_images.py
echo ""

# Step 2: Generate Site
echo "🏗️  Step 2/4: Generating website..."
python3 generate_site.py
echo ""

# Step 3: Git Add & Commit
echo "📝 Step 3/4: Committing changes..."
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

# Step 4: Push to GitHub
echo "🌐 Step 4/4: Pushing to GitHub..."
git push origin main
echo ""

echo "================================"
echo "✨ Deployment Complete!"
echo ""
echo "Your portfolio will be live in ~1 minute at:"
echo "https://Sensibleprat.github.io/photo_portfolio/"
echo ""
