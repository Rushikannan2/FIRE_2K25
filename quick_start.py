#!/usr/bin/env python3
"""
CryptoQ Hugging Face Quick Start
One-click setup and upload for all your models
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show progress."""
    print(f"[RUNNING] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAILED] {description}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("CryptoQ Hugging Face Quick Start")
    print("=" * 50)
    
    # Step 1: Install dependencies
    print("\nSTEP 1: Installing dependencies...")
    packages = [
        "huggingface_hub[cli]",
        "requests", 
        "tqdm"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"[ERROR] Failed to install {package}")
            return False
    
    # Step 2: Check if models exist
    print("\nSTEP 2: Checking model files...")
    models_dir = Path("models")
    if not models_dir.exists():
        print("[ERROR] Models directory not found!")
        print("Please ensure your models are in: models/Level1-3/Fold1-5/model.pth")
        return False
    
    # Count model files
    model_count = 0
    for level in ["Level1", "Level2", "Level3"]:
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            model_file = models_dir / level / fold / "model.pth"
            if model_file.exists():
                model_count += 1
                print(f"[FOUND] {level}/{fold}/model.pth")
    
    print(f"\nFound {model_count}/15 model files")
    
    if model_count == 0:
        print("[ERROR] No model files found!")
        return False
    
    # Step 3: Authenticate with Hugging Face
    print("\nSTEP 3: Hugging Face authentication...")
    print("You need to authenticate with Hugging Face.")
    print("This will open a browser window.")
    
    auth_cmd = "hf auth login"
    print(f"Running: {auth_cmd}")
    
    try:
        # Run authentication interactively
        subprocess.run(auth_cmd.split(), check=True)
        print("[SUCCESS] Authentication successful!")
    except subprocess.CalledProcessError:
        print("[ERROR] Authentication failed!")
        print("Please run manually: hf auth login")
        return False
    
    # Step 4: Upload models
    print("\nSTEP 4: Uploading models to Hugging Face...")
    if not run_command("python upload_models.py", "Uploading all models"):
        print("[ERROR] Upload failed!")
        return False
    
    # Step 5: Test download
    print("\nSTEP 5: Testing download...")
    if not run_command("python download_models_hf.py", "Testing download"):
        print("[ERROR] Download test failed!")
        return False
    
    # Success!
    print("\n" + "=" * 50)
    print("SUCCESS! Your models are now on Hugging Face!")
    print("=" * 50)
    print("[OK] Dependencies installed")
    print("[OK] Hugging Face authenticated") 
    print("[OK] Models uploaded")
    print("[OK] Download tested")
    print("\nRepository: https://huggingface.co/rushikannan/FIRE_CryptoQA")
    print("\nNext steps:")
    print("1. Update render.yaml to use download_models_hf.py")
    print("2. Deploy to Render - no more Google Drive issues!")
    print("=" * 50)

if __name__ == "__main__":
    main()
