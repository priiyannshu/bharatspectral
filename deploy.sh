#!/data/data/com.termux/files/usr/bin/bash
# deploy.sh - Rebuilds BharatSpectral complete ecosystem and deploys to Cloudflare Pages

set -e

# Resolve directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/presentation" ]; then
  REPO_ROOT="$SCRIPT_DIR"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

echo "=========================================================="
echo "🚀 BharatSpectral DSSI Ecosystem Deployment"
echo "=========================================================="

echo "1. Rebuilding full site & assets (PPTX, PDFs, HTML Decks, Benchmarks)..."
python3 "$REPO_ROOT/build_site.py"

echo "2. Deploying complete ecosystem to Cloudflare Pages (bharatspectral)..."
npx wrangler pages deploy "$REPO_ROOT/dist" --project-name=bharatspectral --branch=main --commit-dirty=true

echo "=========================================================="
echo "✅ BharatSpectral Ecosystem Deployment Complete!"
echo "🌐 Live Production URL: https://bharatspectral.pages.dev/"
echo "=========================================================="
