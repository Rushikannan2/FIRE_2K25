#!/usr/bin/env python3
"""
Model Download Script for CryptoQ Sentiment Analyzer
Downloads all 15 model files from Google Drive to the appropriate folders.
"""

import os
import sys
from pathlib import Path

try:
    import gdown
except ImportError:
    print("ERROR: gdown is not installed. Please install it using:")
    print("pip install gdown")
    sys.exit(1)

def create_directories():
    """Create the required directory structure if it doesn't exist."""
    base_path = Path("models")
    
    for level in ["Level1", "Level2", "Level3"]:
        level_path = base_path / level
        level_path.mkdir(parents=True, exist_ok=True)
        
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            fold_path = level_path / fold
            fold_path.mkdir(parents=True, exist_ok=True)
    
    print("SUCCESS: Directory structure created successfully!")

def download_model(url, output_path, description):
    """Download a single model file with error handling."""
    try:
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"SKIPPING {description} - file already exists")
            return True
        
        print(f"DOWNLOADING {description}...")
        gdown.download(url, output_path, quiet=False)
        
        # Verify the file was downloaded
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"SUCCESS: Downloaded {description}")
            return True
        else:
            print(f"FAILED: {description} - file is empty or doesn't exist")
            return False
            
    except Exception as e:
        print(f"ERROR downloading {description}: {str(e)}")
        return False

def main():
    """Main function to download all model files."""
    print("Starting CryptoQ Model Download Process...")
    print("=" * 60)
    
    # Create directory structure
    create_directories()
    print()
    
    # Define all download URLs and their target paths
    downloads = [
        # Level 1 Models
        ("https://drive.google.com/uc?id=135Bantj4cToGl5e7d5pfJg1VDN1B2Rkq", "models/Level1/Fold1/model.pth", "Level1/Fold1"),
        ("https://drive.google.com/uc?id=1kpPEG9yM6QEEa_bpfWiQHAkcqKUqfZC9", "models/Level1/Fold2/model.pth", "Level1/Fold2"),
        ("https://drive.google.com/uc?id=1mTlSi50_xaAc3m6m38BghmUD8jrDJcoD", "models/Level1/Fold3/model.pth", "Level1/Fold3"),
        ("https://drive.google.com/uc?id=1IKttgCyFPiYzoAhTscasnBjWeRcZD1kY", "models/Level1/Fold4/model.pth", "Level1/Fold4"),
        ("https://drive.google.com/uc?id=19va4SIYdG8VF31VF1zot82UVPZmWDz5j", "models/Level1/Fold5/model.pth", "Level1/Fold5"),
        
        # Level 2 Models
        ("https://drive.google.com/uc?id=183l8s6y6O097_tOmD1AhZIgOTwg5l9qt", "models/Level2/Fold1/model.pth", "Level2/Fold1"),
        ("https://drive.google.com/uc?id=1hFZaI5DNr-BWuDXnMeH1eDNIdvxFTtgZ", "models/Level2/Fold2/model.pth", "Level2/Fold2"),
        ("https://drive.google.com/uc?id=1Y43fYp1VIk6XcFEBMbtG2--rfi3yRcW3", "models/Level2/Fold3/model.pth", "Level2/Fold3"),
        ("https://drive.google.com/uc?id=1gTDjO3LBtqfIexVlk4KKEhm2Jvt9UpTd", "models/Level2/Fold4/model.pth", "Level2/Fold4"),
        ("https://drive.google.com/uc?id=1ZCMC1KizUIOXSaHdFeqsCuoedzUDZoJ_", "models/Level2/Fold5/model.pth", "Level2/Fold5"),
        
        # Level 3 Models
        ("https://drive.google.com/uc?id=1Evvmn5EKc2oDD3wtnSPEtUUt4YCl0eUI", "models/Level3/Fold1/model.pth", "Level3/Fold1"),
        ("https://drive.google.com/uc?id=1fqZ1OOdVOPAQ3CIi0LMCpAMuz6UbPGgx", "models/Level3/Fold2/model.pth", "Level3/Fold2"),
        ("https://drive.google.com/uc?id=1GRqOjOAO1qOfHWtmpW1tm8690huuCOPQ", "models/Level3/Fold3/model.pth", "Level3/Fold3"),
        ("https://drive.google.com/uc?id=1tt0s2RJ2G9YfiAIOsqYhXhfPGCbcrqHX", "models/Level3/Fold4/model.pth", "Level3/Fold4"),
        ("https://drive.google.com/uc?id=1nmCEKJvSptND9HNanM6Rxv5Q2ExAN134", "models/Level3/Fold5/model.pth", "Level3/Fold5"),
    ]
    
    # Download all models
    successful_downloads = 0
    total_downloads = len(downloads)
    
    for i, (url, output_path, description) in enumerate(downloads, 1):
        print(f"[{i}/{total_downloads}] Processing {description}...")
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if download_model(url, output_path, description):
            successful_downloads += 1
        
        print("-" * 40)
    
    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Successfully downloaded: {successful_downloads}/{total_downloads} models")
    
    if successful_downloads == total_downloads:
        print("SUCCESS: All model files have been downloaded successfully!")
        print("You can now use them locally without pushing to GitHub.")
    else:
        print(f"WARNING: {total_downloads - successful_downloads} downloads failed. Please check the error messages above.")
        print("You can run this script again to retry failed downloads.")
    
    print("\nModel files are stored in:")
    print("   models/Level1/Fold1-5/")
    print("   models/Level2/Fold1-5/")
    print("   models/Level3/Fold1-5/")

if __name__ == "__main__":
    main()
