#!/usr/bin/env python3
"""
Python startup script for CryptoQ Django app on Render
"""

import os
import sys
import subprocess

def main():
    print("Starting CryptoQ Django application...")
    
    # Change to Django project directory
    django_dir = "CryptoQWeb"
    
    if not os.path.exists(django_dir):
        print(f"ERROR: {django_dir} directory not found!")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for item in os.listdir("."):
            print(f"  {item}")
        sys.exit(1)
    
    # Change to Django directory
    os.chdir(django_dir)
    
    if not os.path.exists("manage.py"):
        print("ERROR: manage.py not found!")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for item in os.listdir("."):
            print(f"  {item}")
        sys.exit(1)
    
    # Get port from environment
    port = os.environ.get("PORT", "8000")
    
    print(f"Starting Django server on port {port}...")
    
    # Start Django server
    try:
        subprocess.run([
            sys.executable, "manage.py", "runserver", f"0.0.0.0:{port}"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Django server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


