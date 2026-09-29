#!/data/data/com.termux/files/usr/bin/bash
# deploy.sh - Rebuilds BharatSpectral 19-slide pinboard presentation and deploys to Cloudflare Pages

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR/presentation" ]; then
  PRES_DIR="$SCRIPT_DIR/presentation"
  REPO_ROOT="$SCRIPT_DIR"
else
  PRES_DIR="$SCRIPT_DIR"
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

echo "=========================================================="
echo "📌 BharatSpectral 19-Slide Pinboard Deck Deployment"
echo "=========================================================="

echo "1. Generating high-resolution scientific & comic assets..."
python3 "$PRES_DIR/generate_assets.py"

echo "2. Rebuilding 19-slide PowerPoint deck (.pptx)..."
python3 "$PRES_DIR/build_deck.py"

echo "3. Rebuilding 19-slide HTML pinboard deck (index.html)..."
python3 "$PRES_DIR/build_html_pinboard_deck.py"

echo "4. Syncing empirical figures into presentation..."
mkdir -p "$PRES_DIR/outputs"
cp -r "$REPO_ROOT/outputs/figures" "$PRES_DIR/outputs/"

echo "5. Deploying to Cloudflare Pages (bharatspectral)..."
npx wrangler pages deploy "$PRES_DIR" --project-name=bharatspectral --branch=main --commit-dirty=true

echo "=========================================================="
echo "✅ BharatSpectral Pinboard Presentation Deployment Complete!"
echo "🌐 Live URL: https://bharatspectral.pages.dev/"
echo "=========================================================="
