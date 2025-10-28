#!/usr/bin/env python3
"""
Enhanced Model Download Script for CryptoQ Sentiment Analyzer
Downloads all 15 model files from Google Drive with robust error handling.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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

def extract_file_id(url):
    """Extract file ID from Google Drive URL."""
    if 'id=' in url:
        return url.split('id=')[1].split('&')[0]
    elif '/file/d/' in url:
        return url.split('/file/d/')[1].split('/')[0]
    else:
        return None

def download_with_requests(file_id, output_path, description, max_retries=3):
    """Download file using requests with proper Google Drive API."""
    for attempt in range(max_retries):
        try:
            print(f"DOWNLOADING {description} (attempt {attempt + 1}/{max_retries})...")
            
            # Method 1: Direct download URL
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(download_url, headers=headers, stream=True, timeout=30)
            
            if response.status_code == 200:
                # Check if we got a confirmation page (for large files)
                if 'download_warning' in response.text or 'virus scan' in response.text.lower():
                    # Extract confirmation token
                    confirm_token = None
                    for line in response.text.split('\n'):
                        if 'confirm=' in line:
                            confirm_token = line.split('confirm=')[1].split('&')[0]
                            break
                    
                    if confirm_token:
                        download_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
                        response = requests.get(download_url, headers=headers, stream=True, timeout=30)
                
                # Download the file
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Progress indicator
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='', flush=True)
                
                print()  # New line after progress
                
                # Verify download
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    file_size = os.path.getsize(output_path)
                    print(f"SUCCESS: Downloaded {description} ({file_size:,} bytes)")
                    return True
                else:
                    print(f"FAILED: {description} - file is empty")
                    return False
                    
            else:
                print(f"FAILED: {description} - HTTP {response.status_code}")
                if attempt < max_retries - 1:
                    print(f"  Retrying in 5 seconds...")
                    time.sleep(5)
                    
        except requests.exceptions.RequestException as e:
            print(f"ERROR downloading {description}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"  Retrying in 5 seconds...")
                time.sleep(5)
        except Exception as e:
            print(f"ERROR downloading {description}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"  Retrying in 5 seconds...")
                time.sleep(5)
    
    return False

def download_model(url, output_path, description):
    """Download a single model file with multiple methods."""
    try:
        # Check if file already exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"SKIPPING {description} - file already exists ({file_size:,} bytes)")
            return True
        
        # Extract file ID
        file_id = extract_file_id(url)
        if not file_id:
            print(f"ERROR: Could not extract file ID from {url}")
            return False
        
        # Try requests method first
        if download_with_requests(file_id, output_path, description):
            return True
        
        # Fallback to gdown if available
        try:
            import gdown
            print(f"FALLBACK: Trying gdown for {description}...")
            gdown.download(url, output_path, quiet=False)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path)
                print(f"SUCCESS: Downloaded {description} via gdown ({file_size:,} bytes)")
                return True
        except ImportError:
            print("gdown not available for fallback")
        except Exception as e:
            print(f"gdown fallback failed: {str(e)}")
        
        print(f"FAILED: {description} - all download methods failed")
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
    failed_downloads = []

    for i, (description, url) in enumerate(model_urls.items(), 1):
        output_path = Path("models") / description / "model.pth"
        print(f"[{i}/{total_downloads}] Processing {description}...")
        
        if download_model(url, output_path, description):
            successful_downloads += 1
        else:
            failed_downloads.append(description)
        
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
        print(f"WARNING: {total_downloads - successful_downloads} downloads failed.")
        print("Failed downloads:")
        for failed in failed_downloads:
            print(f"  - {failed}")
        print("\nTo fix failed downloads:")
        print("1. Check Google Drive file permissions (set to 'Anyone with the link')")
        print("2. Verify file IDs are correct")
        print("3. Run the script again to retry failed downloads")
    
    print("\nModel files are stored in:")
    print("   models/Level1/Fold1-5/")
    print("   models/Level2/Fold1-5/")
    print("   models/Level3/Fold1-5/")

if __name__ == "__main__":
    main()
