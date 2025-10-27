#!/usr/bin/env python3
"""
Hugging Face Model Download Script for CryptoQ Sentiment Analyzer
Downloads all .pth model files from Hugging Face repository to local folders.

Usage:
    python download_models_hf.py

Requirements:
    1. Install: pip install huggingface_hub
    2. Ensure models/ directory structure exists
"""

import os
import sys
from pathlib import Path
import requests
from tqdm import tqdm

# Configuration
HF_REPO = "rushikannan/FIRE_CryptoQA"
MODELS_BASE_DIR = Path("models")
TOTAL_EXPECTED_FILES = 15  # 3 levels × 5 folds

def create_directories():
    """Create the required directory structure if it doesn't exist."""
    print("📁 Creating directory structure...")
    
    for level in ["Level1", "Level2", "Level3"]:
        level_path = MODELS_BASE_DIR / level
        level_path.mkdir(parents=True, exist_ok=True)
        
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            fold_path = level_path / fold
            fold_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure created successfully!")

def download_file_from_hf(hf_path, local_path, description):
    """Download a single file from Hugging Face."""
    print(f"\n📥 Downloading {description}...")
    print(f"   HF Path: {hf_path}")
    print(f"   Local Path: {local_path}")
    
    # Check if file already exists and is not empty
    if local_path.exists() and local_path.stat().st_size > 0:
        print(f"   ⏭️  SKIPPING: {description} already exists and is not empty")
        return True
    
    try:
        # Construct Hugging Face download URL
        url = f"https://huggingface.co/{HF_REPO}/resolve/main/{hf_path}"
        print(f"   URL: {url}")
        
        # Download with progress bar
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(local_path, 'wb') as f:
            with tqdm(total=total_size, unit='iB', unit_scale=True, 
                     desc=f"   Downloading {description}", leave=False) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Verify download
        if local_path.exists() and local_path.stat().st_size > 0:
            file_size_mb = local_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ SUCCESS: {description} downloaded ({file_size_mb:.1f} MB)")
            return True
        else:
            print(f"   ❌ FAILED: {description} - downloaded file is empty")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ ERROR: {description} - {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {description} - {str(e)}")
        return False

def main():
    """Main function to orchestrate the download process."""
    print("🚀 CryptoQ Model Download from Hugging Face")
    print("=" * 50)
    print(f"Source Repository: {HF_REPO}")
    print(f"Local Directory: {MODELS_BASE_DIR}")
    print("=" * 50)
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Download all model files
    print(f"\n📥 Starting download of {TOTAL_EXPECTED_FILES} files...")
    print("=" * 50)
    
    successful_downloads = 0
    failed_downloads = 0
    
    for level in ["Level1", "Level2", "Level3"]:
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            description = f"{level}/{fold}"
            hf_path = f"models/{level}/{fold}/model.pth"
            local_path = MODELS_BASE_DIR / level / fold / "model.pth"
            
            if download_file_from_hf(hf_path, local_path, description):
                successful_downloads += 1
            else:
                failed_downloads += 1
    
    # Step 3: Summary
    print("\n" + "=" * 50)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 50)
    print(f"Total files expected: {TOTAL_EXPECTED_FILES}")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    
    if successful_downloads == TOTAL_EXPECTED_FILES:
        print("\n🎉 SUCCESS: All model files downloaded successfully!")
        print("✅ You can now use the models locally without pushing to GitHub.")
    elif successful_downloads > 0:
        print(f"\n⚠️  PARTIAL SUCCESS: {successful_downloads}/{TOTAL_EXPECTED_FILES} files downloaded")
        print("Please check the error messages above and retry failed downloads.")
    else:
        print("\n❌ FAILED: No files were downloaded successfully")
        print("Please check your internet connection and try again.")
    
    print("\nModel files are stored in:")
    print("   models/Level1/Fold1-5/")
    print("   models/Level2/Fold1-5/")
    print("   models/Level3/Fold1-5/")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
