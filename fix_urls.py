#!/usr/bin/env python3
"""
URL Converter for Google Drive Files
Converts direct download URLs to proper sharing URLs
"""

import json

# Your current file IDs (extracted from your URLs)
file_ids = {
    "Level1/Fold1": "135Bantj4cToGl5e7d5pfJg1VDN1B2Rkq",
    "Level1/Fold2": "1kpPEG9yM6QEEa_bpfWiQHAkcqKUqfZC9",
    "Level1/Fold3": "1mTlSi50_xaAc3m6m38BghmUD8jrDJcoD",
    "Level1/Fold4": "1IKttgCyFPiYzoAhTscasnBjWeRcZD1kY",
    "Level1/Fold5": "19va4SIYdG8VF31VF1zot82UVPZmWDz5j",
    "Level2/Fold1": "183l8s6y6O097_tOmD1AhZIgOTwg5l9qt",
    "Level2/Fold2": "1hFZaI5DNr-BWuDXnMeH1eDNIdvxFTtgZ",
    "Level2/Fold3": "1Y43fYp1VIk6XcFEBMbtG2--rfi3yRcW3",
    "Level2/Fold4": "1gTDjO3LBtqfIexVlk4KKEhm2Jvt9UpTd",
    "Level2/Fold5": "1ZCMC1KizUIOXSaHdFeqsCuoedzUDZoJ_",
    "Level3/Fold1": "1Evvmn5EKc2oDD3wtnSPEtUUt4YCl0eUI",
    "Level3/Fold2": "1fqZ1OOdVOPAQ3CIi0LMCpAMuz6UbPGgx",
    "Level3/Fold3": "1GRqOjOAO1qOfHWtmpW1tm8690huuCOPQ",
    "Level3/Fold4": "1tt0s2RJ2G9YfiAIOsqYhXhfPGCbcrqHX",
    "Level3/Fold5": "1nmCEKJvSptND9HNanM6Rxv5Q2ExAN134"
}

# Convert to proper sharing URLs
sharing_urls = {}
for path, file_id in file_ids.items():
    sharing_urls[path] = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

# Create updated config
updated_config = {
    "model_urls": sharing_urls,
    "model_info": {
        "total_models": 15,
        "model_size_mb": 567,
        "total_size_gb": 8.5,
        "description": "CryptoQ Sentiment Analysis Models - Level1, Level2, Level3 with 5 folds each"
    }
}

# Save updated config
with open('model_config_updated.json', 'w') as f:
    json.dump(updated_config, f, indent=2)

print("✅ Created model_config_updated.json with proper sharing URLs")
print("\n📋 Next steps:")
print("1. Set all Google Drive files to 'Anyone with the link'")
print("2. Replace model_config.json with model_config_updated.json")
print("3. Test the download script")

# Also create direct download URLs as backup
direct_urls = {}
for path, file_id in file_ids.items():
    direct_urls[path] = f"https://drive.google.com/uc?export=download&id={file_id}"

direct_config = {
    "model_urls": direct_urls,
    "model_info": updated_config["model_info"]
}

with open('model_config_direct.json', 'w') as f:
    json.dump(direct_config, f, indent=2)

print("✅ Also created model_config_direct.json with direct download URLs")


