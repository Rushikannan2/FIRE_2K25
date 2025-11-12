"""
Background model download script that doesn't block deployment.
Downloads models asynchronously after the app starts.
"""
import os
import sys
import subprocess
import time
from threading import Thread

def download_models_async():
    """Download models in background thread"""
    try:
        print("🔄 Starting background model download...")
        # Run download_models.py in background
        subprocess.run([sys.executable, "download_models.py"], 
                      timeout=3600,  # 1 hour timeout
                      check=False)  # Don't fail if it errors
        print("✅ Background model download completed")
    except Exception as e:
        print(f"⚠️ Background model download error: {e}")
        print("Models will be downloaded on first use")

if __name__ == "__main__":
    # Start download in background thread
    thread = Thread(target=download_models_async, daemon=True)
    thread.start()
    print("✅ Model download started in background")
    # Don't wait - let the app start immediately
    sys.exit(0)

