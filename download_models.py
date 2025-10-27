#!/usr/bin/env python3
"""
Model Download Script for CryptoQ Sentiment Analyzer
Downloads all 15 model files from Google Drive to the appropriate folders.
"""

import os
import sys
import json
from pathlib import Path

try:
    import gdown
except ImportError:
    print("ERROR: gdown is not installed. Please install it using:")
    print("pip install gdown")
    sys.exit(1)

def load_model_config():
    """Load model configuration from JSON file."""
    try:
        with open('model_config.json', 'r') as f:
            config = json.load(f)
        return config['model_urls']
    except FileNotFoundError:
        print("ERROR: model_config.json not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON in model_config.json!")
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
    
    # Load model configuration
    model_urls = load_model_config()
    
    # Create directory structure
    create_directories()
    print()
    
    total_downloads = len(model_urls)
    successful_downloads = 0

    for i, (description, url) in enumerate(model_urls.items(), 1):
        output_path = Path("models") / description / "model.pth"
        print(f"[{i}/{total_downloads}] Processing {description}...")
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
