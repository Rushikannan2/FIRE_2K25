#!/usr/bin/env python3
"""
Setup script for Hugging Face model management
Installs required dependencies and provides setup instructions.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 CryptoQ Hugging Face Setup")
    print("=" * 40)
    
    # Required packages
    packages = [
        "huggingface_hub[cli]",
        "requests",
        "tqdm"
    ]
    
    print("📦 Installing required packages...")
    
    for package in packages:
        print(f"   Installing {package}...")
        if install_package(package):
            print(f"   ✅ {package} installed successfully")
        else:
            print(f"   ❌ Failed to install {package}")
            return False
    
    print("\n✅ All packages installed successfully!")
    print("\n📋 Next Steps:")
    print("1. Authenticate with Hugging Face:")
    print("   hf auth login")
    print("\n2. Upload your models:")
    print("   python upload_models.py")
    print("\n3. Download models (for deployment):")
    print("   python download_models_hf.py")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()

