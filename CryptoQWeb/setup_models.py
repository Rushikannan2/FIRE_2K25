#!/usr/bin/env python3
"""
Script to copy model files from the models directory to the Django project
"""

import os
import shutil
from pathlib import Path

def setup_models():
    """Copy model files from the parent models directory to the Django project"""
    
    # Source and destination directories
    source_dir = Path("../models")
    dest_dir = Path("models")
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)
    
    # Model files to copy
    model_files = [
        "level1_fold1.pth", "level1_fold2.pth", "level1_fold3.pth", "level1_fold4.pth", "level1_fold5.pth",
        "level2_fold1.pth", "level2_fold2.pth", "level2_fold3.pth", "level2_fold4.pth", "level2_fold5.pth",
        "level3_fold1.pth", "level3_fold2.pth", "level3_fold3.pth", "level3_fold4.pth", "level3_fold5.pth"
    ]
    
    copied_count = 0
    
    for model_file in model_files:
        source_path = source_dir / model_file
        dest_path = dest_dir / model_file
        
        if source_path.exists():
            try:
                shutil.copy2(source_path, dest_path)
                print(f"[OK] Copied {model_file}")
                copied_count += 1
            except Exception as e:
                print(f"[ERROR] Error copying {model_file}: {e}")
        else:
            print(f"[WARNING] {model_file} not found in {source_dir}")
    
    print(f"\nCopied {copied_count} model files to {dest_dir}")
    
    if copied_count == 0:
        print("\nNo model files found. The system will use fallback analysis.")
        print("To use the AI models, place the .pth files in the models/ directory.")
    else:
        print(f"\nSetup complete! {copied_count} model files are now available.")

if __name__ == "__main__":
    setup_models()
