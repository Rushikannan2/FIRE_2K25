#!/usr/bin/env python3
"""
Advanced Google Drive Test Script
Tests different URL formats and handles Google Drive's specific behavior
"""

import requests
import json
import time

def test_google_drive_file(file_id, description):
    """Test Google Drive file with multiple URL formats"""
    print(f"\nTesting {description} (ID: {file_id})")
    
    # Different URL formats to test
    urls_to_test = [
        f"https://drive.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/file/d/{file_id}/view?usp=sharing",
        f"https://drive.google.com/file/d/{file_id}/view",
        f"https://drive.google.com/uc?id={file_id}&export=download",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"  Test {i}: {url}")
        try:
            # First, try HEAD request
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            print(f"    HEAD: HTTP {response.status_code}")
            
            if response.status_code == 200:
                # Try GET request to see if we get actual content
                get_response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                print(f"    GET: HTTP {get_response.status_code}")
                
                if get_response.status_code == 200:
                    content_length = len(get_response.content)
                    print(f"    Content length: {content_length} bytes")
                    
                    if content_length > 1000:  # Likely a real file
                        print(f"    SUCCESS: {description} is accessible via this URL!")
                        return url
                    elif "google" in get_response.text.lower() and "access" in get_response.text.lower():
                        print(f"    FAILED: Access denied page")
                    else:
                        print(f"    UNKNOWN: Got content but might be error page")
                else:
                    print(f"    FAILED: GET request failed")
            else:
                print(f"    FAILED: HEAD request failed")
                
        except Exception as e:
            print(f"    ERROR: {str(e)}")
        
        time.sleep(1)  # Be nice to Google's servers
    
    print(f"  FAILED: {description} not accessible with any URL format")
    return None

def main():
    """Test all model files with different URL formats"""
    print("Advanced Google Drive File Accessibility Test")
    print("=" * 60)
    
    # Load file IDs
    with open('model_config.json', 'r') as f:
        config = json.load(f)
    
    working_urls = {}
    total_files = len(config['model_urls'])
    
    for description, url in config['model_urls'].items():
        # Extract file ID
        if 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
        else:
            print(f"ERROR: Could not extract file ID from {url}")
            continue
            
        working_url = test_google_drive_file(file_id, description)
        if working_url:
            working_urls[description] = working_url
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Working files: {len(working_urls)}/{total_files}")
    
    if len(working_urls) == total_files:
        print("SUCCESS: All files are accessible!")
        print("\nWorking URLs:")
        for desc, url in working_urls.items():
            print(f"  {desc}: {url}")
    elif len(working_urls) > 0:
        print(f"PARTIAL: {len(working_urls)} files are accessible")
        print("\nWorking URLs:")
        for desc, url in working_urls.items():
            print(f"  {desc}: {url}")
        print(f"\nStill need to fix: {total_files - len(working_urls)} files")
    else:
        print("FAILED: No files are accessible")
        print("\nTROUBLESHOOTING STEPS:")
        print("1. Go to Google Drive")
        print("2. Right-click each file -> Share")
        print("3. Make sure it says 'Anyone with the link can view'")
        print("4. Click 'Copy link' to get the correct sharing URL")
        print("5. Update model_config.json with the new URLs")
        print("6. Run this test again")

if __name__ == "__main__":
    main()


