#!/usr/bin/env python3
"""
Comprehensive Google Drive Troubleshooting Script
Tests different approaches to download files
"""

import requests
import json
import time
import os

def test_single_file(file_id, description):
    """Test a single Google Drive file with multiple methods"""
    print(f"\n{'='*60}")
    print(f"Testing {description} (ID: {file_id})")
    print(f"{'='*60}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Method 1: Direct download URL
    print("\nMethod 1: Direct download URL")
    url1 = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"URL: {url1}")
    
    try:
        response = requests.get(url1, headers=headers, timeout=30, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Content-Length: {len(response.content)}")
        
        if response.status_code == 200:
            if len(response.content) > 1000000:  # > 1MB
                print("SUCCESS: Large file detected - likely the actual model!")
                return True
            elif "google" in response.text.lower() and "access" in response.text.lower():
                print("FAILED: Access denied page")
            elif "virus" in response.text.lower() or "scan" in response.text.lower():
                print("INFO: Virus scan page detected - need confirmation token")
                # Try to extract confirmation token
                if "confirm=" in response.text:
                    confirm_token = response.text.split("confirm=")[1].split("&")[0]
                    print(f"Found confirmation token: {confirm_token}")
                    
                    # Try with confirmation token
                    url_with_confirm = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
                    print(f"Trying with confirmation: {url_with_confirm}")
                    
                    confirm_response = requests.get(url_with_confirm, headers=headers, timeout=30)
                    print(f"Confirmation status: {confirm_response.status_code}")
                    print(f"Confirmation content length: {len(confirm_response.content)}")
                    
                    if len(confirm_response.content) > 1000000:
                        print("SUCCESS: Confirmation worked!")
                        return True
            else:
                print("UNKNOWN: Got content but unclear what it is")
        else:
            print(f"FAILED: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
    # Method 2: Alternative URL format
    print("\nMethod 2: Alternative URL format")
    url2 = f"https://drive.google.com/uc?id={file_id}&export=download"
    print(f"URL: {url2}")
    
    try:
        response = requests.get(url2, headers=headers, timeout=30, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Content-Length: {len(response.content)}")
        
        if response.status_code == 200 and len(response.content) > 1000000:
            print("SUCCESS: Alternative URL worked!")
            return True
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
    # Method 3: Try with different headers
    print("\nMethod 3: Different headers")
    headers2 = {
        'User-Agent': 'curl/7.68.0',
        'Accept': '*/*'
    }
    
    try:
        response = requests.get(url1, headers=headers2, timeout=30, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Content-Length: {len(response.content)}")
        
        if response.status_code == 200 and len(response.content) > 1000000:
            print("SUCCESS: Different headers worked!")
            return True
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
    print(f"\nFAILED: {description} not accessible with any method")
    return False

def main():
    """Test all files and provide detailed troubleshooting"""
    print("Google Drive Comprehensive Troubleshooting")
    print("=" * 60)
    
    # Load file IDs
    with open('model_config.json', 'r') as f:
        config = json.load(f)
    
    working_files = []
    failed_files = []
    
    for description, url in config['model_urls'].items():
        # Extract file ID
        if 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
        else:
            print(f"ERROR: Could not extract file ID from {url}")
            failed_files.append(description)
            continue
        
        if test_single_file(file_id, description):
            working_files.append(description)
        else:
            failed_files.append(description)
        
        time.sleep(2)  # Be nice to Google's servers
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Working files: {len(working_files)}/{len(config['model_urls'])}")
    print(f"Failed files: {len(failed_files)}/{len(config['model_urls'])}")
    
    if len(working_files) == len(config['model_urls']):
        print("\nSUCCESS: All files are accessible!")
    elif len(working_files) > 0:
        print(f"\nPARTIAL SUCCESS: {len(working_files)} files work")
        print("Working files:")
        for file in working_files:
            print(f"  ✅ {file}")
        print("\nFailed files:")
        for file in failed_files:
            print(f"  ❌ {file}")
    else:
        print("\nFAILED: No files are accessible")
    
    print(f"\n{'='*60}")
    print("TROUBLESHOOTING STEPS")
    print(f"{'='*60}")
    print("1. Go to Google Drive in your browser")
    print("2. Right-click each failed file -> Share")
    print("3. Make sure it says 'Anyone with the link can view'")
    print("4. If not, click 'Change to anyone with the link'")
    print("5. Set permission to 'Viewer' (not Editor)")
    print("6. Click 'Done'")
    print("7. Repeat for all failed files")
    print("8. Run this script again to verify")

if __name__ == "__main__":
    main()


