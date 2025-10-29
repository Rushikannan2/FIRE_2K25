#!/usr/bin/env python3
"""
Optimized Model Download Script for Render
- Caches models to avoid re-downloading
- Downloads only if models don't exist
- Uses parallel downloads for faster processing
"""

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from huggingface_hub import hf_hub_download

# Configuration
HF_REPO = "rushikannan/FIRE_CryptoQA"
MODELS_BASE_DIR = Path("models")
MAX_WORKERS = 3  # Limit concurrent downloads to avoid overwhelming Render

def create_directories():
    """Create directory structure if it doesn't exist."""
    for level in ["Level1", "Level2", "Level3"]:
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            (MODELS_BASE_DIR / level / fold).mkdir(parents=True, exist_ok=True)

def download_model(args):
    """Download a single model file."""
    level, fold, token = args
    filename = f"models/{level}/{fold}/model.pth"
    local_path = MODELS_BASE_DIR / level / fold / "model.pth"
    
    # Skip if file already exists and is not empty
    if local_path.exists() and local_path.stat().st_size > 0:
        print(f"⏭️  SKIPPING {level}/{fold} - already exists")
        return True
    
    try:
        print(f"⬇️  Downloading {level}/{fold}...")
        hf_hub_download(
            repo_id=HF_REPO,
            filename=filename,
            token=token,
            local_dir=f"models/{level}/{fold}",
            local_dir_use_symlinks=False
        )
        print(f"✅ SUCCESS: {level}/{fold}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {level}/{fold} — {e}")
        return False

def main():
    """Main function with parallel downloads."""
    print("🚀 Optimized CryptoQ Model Download Process")
    print("=" * 60)
    
    # Get token from environment
    token = os.getenv("HF_TOKEN")
    if not token:
        print("❌ ERROR: HF_TOKEN environment variable not set!")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Prepare download arguments
    levels = ["Level1", "Level2", "Level3"]
    folds = ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]
    download_args = [(level, fold, token) for level in levels for fold in folds]
    
    # Download models in parallel
    successful_downloads = 0
    total_downloads = len(download_args)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_args = {executor.submit(download_model, args): args for args in download_args}
        
        for future in as_completed(future_to_args):
            if future.result():
                successful_downloads += 1
    
    # Summary
    print("=" * 60)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total models: {total_downloads}")
    print(f"Successful: {successful_downloads}")
    print(f"Failed: {total_downloads - successful_downloads}")
    
    if successful_downloads == total_downloads:
        print("🎉 All models downloaded successfully!")
    else:
        print(f"⚠️  {total_downloads - successful_downloads} downloads failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
