#!/usr/bin/env python
"""
Verification script to ensure all static images are properly collected
"""
import os
from pathlib import Path

# Get BASE_DIR
BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = BASE_DIR / 'staticfiles'
ASSETS_DIR = BASE_DIR / 'assets'

required_images = [
    'CryptoQ.jpeg',
    'FIRE.jpg',
    'IIITKottayam_Summer_Internship.jpg',
]

print("=" * 60)
print("STATIC FILES VERIFICATION")
print("=" * 60)

print(f"\nBASE_DIR: {BASE_DIR}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
print(f"ASSETS_DIR: {ASSETS_DIR}")

print("\n" + "=" * 60)
print("Checking source images in assets/")
print("=" * 60)
all_assets_exist = True
for img in required_images:
    img_path = ASSETS_DIR / img
    exists = img_path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {img}: {exists}")
    if not exists:
        all_assets_exist = False

print("\n" + "=" * 60)
print("Checking collected images in staticfiles/")
print("=" * 60)
all_static_exist = True
for img in required_images:
    img_path = STATIC_ROOT / img
    exists = img_path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {img}: {exists}")
    if not exists:
        all_static_exist = False

print("\n" + "=" * 60)
if all_assets_exist and all_static_exist:
    print("✓ ALL IMAGES VERIFIED - Ready for deployment!")
else:
    print("✗ SOME IMAGES MISSING - Run collectstatic!")
print("=" * 60)

