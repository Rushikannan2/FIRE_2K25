#!/usr/bin/env python3
"""
Hugging Face Model Upload Script for CryptoQ Sentiment Analyzer
Uploads all .pth model files from nested folders to Hugging Face repository.

Usage:
    python upload_models.py

Requirements:
    1. Install: pip install -U "huggingface_hub[cli]"
    2. Authenticate: hf auth login
    3. Ensure models/ directory exists with Level1-3/Fold1-5 structure
"""

import os
import sys
import subprocess
from pathlib import Path
import time

# Configuration
HF_REPO = "rushikannan/FIRE_CryptoQA"
MODELS_BASE_DIR = Path("models")
TOTAL_EXPECTED_FILES = 15  # 3 levels × 5 folds

def check_hf_cli():
    """Check if Hugging Face CLI is installed and authenticated."""
    print("🔍 Checking Hugging Face CLI installation...")
    
    try:
        # Check if hf command exists
        result = subprocess.run(["hf", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ ERROR: Hugging Face CLI not found!")
            print("Please install it with: pip install -U 'huggingface_hub[cli]'")
            return False
        
        print(f"✅ Hugging Face CLI found: {result.stdout.strip()}")
        
        # Check authentication
        auth_result = subprocess.run(["hf", "whoami"], 
                                   capture_output=True, text=True, timeout=10)
        if auth_result.returncode != 0:
            print("❌ ERROR: Not authenticated with Hugging Face!")
            print("Please run: hf auth login")
            return False
        
        print(f"✅ Authenticated as: {auth_result.stdout.strip()}")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Hugging Face CLI check timed out")
        return False
    except FileNotFoundError:
        print("❌ ERROR: Hugging Face CLI not found!")
        print("Please install it with: pip install -U 'huggingface_hub[cli]'")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def find_model_files():
    """Find all model.pth files in the expected directory structure."""
    print(f"\n🔍 Scanning for model files in {MODELS_BASE_DIR}...")
    
    model_files = []
    
    # Expected structure: Level1-3/Fold1-5/model.pth
    for level in ["Level1", "Level2", "Level3"]:
        level_path = MODELS_BASE_DIR / level
        if not level_path.exists():
            print(f"⚠️  Warning: {level_path} directory not found")
            continue
        
        for fold in ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]:
            fold_path = level_path / fold
            model_file = fold_path / "model.pth"
            
            if model_file.exists():
                # Get file size for progress reporting
                file_size = model_file.stat().st_size
                file_size_mb = file_size / (1024 * 1024)
                
                model_files.append({
                    'local_path': model_file,
                    'hf_path': f"models/{level}/{fold}/model.pth",
                    'size_mb': file_size_mb,
                    'description': f"{level}/{fold}"
                })
                print(f"✅ Found: {model_file} ({file_size_mb:.1f} MB)")
            else:
                print(f"⚠️  Missing: {model_file}")
    
    print(f"\n📊 Found {len(model_files)}/{TOTAL_EXPECTED_FILES} model files")
    return model_files

def upload_single_file(file_info):
    """Upload a single model file to Hugging Face."""
    local_path = file_info['local_path']
    hf_path = file_info['hf_path']
    description = file_info['description']
    size_mb = file_info['size_mb']
    
    print(f"\n📤 Uploading {description} ({size_mb:.1f} MB)...")
    print(f"   Local: {local_path}")
    print(f"   HF Path: {hf_path}")
    
    try:
        # Use hf upload command
        cmd = [
            "hf", "upload",
            str(local_path),           # Local file path
            f"{HF_REPO}/{hf_path}",   # Destination in HF repo
            "--repo-type", "model"     # Specify it's a model repo
        ]
        
        print(f"   Command: {' '.join(cmd)}")
        
        # Run upload command with progress
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              timeout=600)  # 10 minute timeout for large files
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description} uploaded successfully!")
            return True
        else:
            print(f"❌ FAILED: {description}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {description} upload timed out (>10 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {description} - {str(e)}")
        return False

def main():
    """Main function to orchestrate the upload process."""
    print("🚀 CryptoQ Model Upload to Hugging Face")
    print("=" * 50)
    print(f"Target Repository: {HF_REPO}")
    print(f"Models Directory: {MODELS_BASE_DIR}")
    print("=" * 50)
    
    # Step 1: Check prerequisites
    if not check_hf_cli():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Step 2: Find model files
    model_files = find_model_files()
    
    if not model_files:
        print("\n❌ No model files found!")
        print("Please ensure your models are in the correct directory structure:")
        print("models/Level1/Fold1/model.pth")
        print("models/Level1/Fold2/model.pth")
        print("... (and so on)")
        sys.exit(1)
    
    # Step 3: Upload files
    print(f"\n📤 Starting upload of {len(model_files)} files...")
    print("=" * 50)
    
    successful_uploads = 0
    failed_uploads = 0
    
    for i, file_info in enumerate(model_files, 1):
        print(f"\n[{i}/{len(model_files)}] Processing {file_info['description']}")
        
        if upload_single_file(file_info):
            successful_uploads += 1
        else:
            failed_uploads += 1
        
        # Small delay between uploads to be nice to HF servers
        if i < len(model_files):
            print("   ⏳ Waiting 2 seconds before next upload...")
            time.sleep(2)
    
    # Step 4: Summary
    print("\n" + "=" * 50)
    print("📊 UPLOAD SUMMARY")
    print("=" * 50)
    print(f"Total files found: {len(model_files)}")
    print(f"Successful uploads: {successful_uploads}")
    print(f"Failed uploads: {failed_uploads}")
    
    if successful_uploads == len(model_files):
        print("\n🎉 SUCCESS: All model files uploaded successfully!")
        print(f"🔗 Repository: https://huggingface.co/{HF_REPO}")
        print("\n✅ You can now update your download script to use Hugging Face URLs!")
        print("   Example: https://huggingface.co/rushikannan/FIRE_CryptoQA/resolve/main/models/Level1/Fold1/model.pth")
    elif successful_uploads > 0:
        print(f"\n⚠️  PARTIAL SUCCESS: {successful_uploads}/{len(model_files)} files uploaded")
        print("Please check the error messages above and retry failed uploads.")
    else:
        print("\n❌ FAILED: No files were uploaded successfully")
        print("Please check your authentication and try again.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
