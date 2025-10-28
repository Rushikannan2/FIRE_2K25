#!/usr/bin/env python3
"""
Quick test script to check Google Drive file accessibility
"""

import requests
import json

def test_file_access(file_id, description):
    """Test if a Google Drive file is accessible"""
    print(f"Testing {description} (ID: {file_id})...")
    
    # Test direct download URL
    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        response = requests.head(direct_url, timeout=10)
        print(f"  Direct URL: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print(f"  SUCCESS: {description} is accessible")
            return True
        else:
            print(f"  FAILED: {description} returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ERROR: {description} - {str(e)}")
        return False

def main():
    """Test all model files"""
    print("Testing Google Drive file accessibility...")
    print("=" * 50)
    
    # Load file IDs from config
    with open('model_config.json', 'r') as f:
        config = json.load(f)
    
    accessible_files = 0
    total_files = len(config['model_urls'])
    
    for description, url in config['model_urls'].items():
        # Extract file ID from URL
        if 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
        else:
            print(f"ERROR: Could not extract file ID from {url}")
            continue
            
        if test_file_access(file_id, description):
            accessible_files += 1
        print()
    
    print("=" * 50)
    print(f"SUMMARY: {accessible_files}/{total_files} files are accessible")
    
    if accessible_files == 0:
        print("\nSOLUTION:")
        print("1. Go to Google Drive")
        print("2. Right-click each file -> Share")
        print("3. Change to 'Anyone with the link'")
        print("4. Set permission to 'Viewer'")
        print("5. Run this test again")
    elif accessible_files < total_files:
        print(f"\n{total_files - accessible_files} files still need permission fixes")
    else:
        print("\nAll files are accessible! You can proceed with deployment.")

if __name__ == "__main__":
    main()
