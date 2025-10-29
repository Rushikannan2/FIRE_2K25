#!/usr/bin/env python
"""
Script to verify static files are properly collected and accessible
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def verify_images():
    """Verify that all required images exist in the assets directory"""
    assets_dir = BASE_DIR / 'assets'
    staticfiles_dir = BASE_DIR / 'staticfiles'
    
    required_images = [
        'CryptoQ.jpeg',
        'FIRE.jpg',
        'IIITKottayam_Summer_Internship.jpg',
        'Task1.jpg'
    ]
    
    print("🔍 Verifying Static Files...")
    print("=" * 50)
    
    # Check assets directory
    print(f"\n📁 Checking assets directory: {assets_dir}")
    if not assets_dir.exists():
        print("❌ ERROR: assets directory does not exist!")
        return False
    
    all_found = True
    for img in required_images:
        img_path = assets_dir / img
        if img_path.exists():
            size = img_path.stat().st_size / 1024  # KB
            print(f"✅ {img} - {size:.2f} KB")
        else:
            print(f"❌ {img} - NOT FOUND")
            all_found = False
    
    # Check staticfiles directory
    print(f"\n📁 Checking staticfiles directory: {staticfiles_dir}")
    if not staticfiles_dir.exists():
        print("⚠️  staticfiles directory does not exist - run collectstatic")
    else:
        for img in required_images:
            img_path = staticfiles_dir / img
            if img_path.exists():
                size = img_path.stat().st_size / 1024  # KB
                print(f"✅ {img} - {size:.2f} KB (collected)")
            else:
                print(f"⚠️  {img} - Not collected yet")
    
    return all_found

if __name__ == '__main__':
    verify_images()

