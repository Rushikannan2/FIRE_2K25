#!/usr/bin/env python3
"""
Final Model Download Script for CryptoQ Sentiment Analyzer from Hugging Face Hub
Downloads all 15 model files from Hugging Face Hub to the appropriate folders.
This replaces the Google Drive download method with a more reliable solution.
"""

import os
import sys
import json
from pathlib import Path
from huggingface_hub import hf_hub_download

# Configuration
HF_REPO_ID = "rushikannan/FIRE_CryptoQA"
MODELS_BASE_DIR = Path("models")

def create_directories():
    """Create the required directory structure if it doesn't exist."""
    print("Creating directory structure...")
    for level in ["Level1", "Level2", "Level3"]:
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            (MODELS_BASE_DIR / level / fold).mkdir(parents=True, exist_ok=True)
    print("SUCCESS: Directory structure created successfully!")

def download_model_from_hf(repo_id, hf_path, local_path, description):
    """Download a single model file from Hugging Face Hub."""
    if local_path.exists() and local_path.stat().st_size > 0:
        print(f"SKIPPING {description} - file already exists and is not empty.")
        return True
    
    print(f"DOWNLOADING {description} from Hugging Face Hub...")
    try:
        # hf_hub_download handles caching and progress automatically
        downloaded_file = hf_hub_download(
            repo_id=repo_id,
            filename=hf_path,
            local_dir=".", # Download to current directory
            local_dir_use_symlinks=False # Ensure actual files are downloaded
        )
        
        if Path(downloaded_file).exists() and Path(downloaded_file).stat().st_size > 0:
            print(f"SUCCESS: Downloaded {description} to {downloaded_file}")
            return True
        else:
            print(f"FAILED: {description} - downloaded file is empty or doesn't exist.")
            return False
    except Exception as e:
        print(f"ERROR downloading {description} from Hugging Face Hub: {e}")
        print("Please ensure the repository and file exist and are accessible.")
        return False

def main():
    """Main function to download all model files from Hugging Face Hub."""
    print("Starting CryptoQ Model Download from Hugging Face Hub...")
    print("=" * 60)
    print(f"Repository: {HF_REPO_ID}")
    print(f"Local directory: {MODELS_BASE_DIR}")
    print("=" * 60)
    
    create_directories()
    print()
    
    total_downloads = 0
    successful_downloads = 0
    
    # Define the expected model paths in the Hugging Face repo
    model_paths = []
    for level in ["Level1", "Level2", "Level3"]:
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            model_paths.append(f"models/{level}/{fold}/model.pth")
    
    total_downloads = len(model_paths)

    for i, hf_path in enumerate(model_paths, 1):
        description = "/".join(hf_path.split('/')[1:-1]) # e.g., Level1/Fold1
        local_output_path = MODELS_BASE_DIR / description / "model.pth"
        
        print(f"[{i}/{total_downloads}] Processing {description}...")
        if download_model_from_hf(HF_REPO_ID, hf_path, local_output_path, description):
            successful_downloads += 1
        
        print("-" * 40)
    
    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Successfully downloaded: {successful_downloads}/{total_downloads} models")
    
    if successful_downloads == total_downloads:
        print("SUCCESS: All model files have been downloaded successfully from Hugging Face Hub!")
        print("You can now use them locally without pushing to GitHub.")
        print("\nModel files are stored in:")
        print(f"   {MODELS_BASE_DIR}/Level1/Fold1-5/")
        print(f"   {MODELS_BASE_DIR}/Level2/Fold1-5/")
        print(f"   {MODELS_BASE_DIR}/Level3/Fold1-5/")
    else:
        print(f"WARNING: {total_downloads - successful_downloads} downloads failed. Please check the error messages above.")
        print("You can run this script again to retry failed downloads.")

if __name__ == "__main__":
    main()
