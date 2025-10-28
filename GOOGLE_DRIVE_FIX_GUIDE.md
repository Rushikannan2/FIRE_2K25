# Google Drive Model Download Fix for Render Deployment

## 🚨 Current Problem
Your Render deployment fails because Google Drive files are not accessible due to permission issues. The error "Access denied" or "file is empty or doesn't exist" occurs because:

1. **Google Drive files are not set to public access**
2. **Large files (>25MB) require confirmation tokens**
3. **Rate limiting and timeout issues**

## 🔧 Solution 1: Fix Google Drive Permissions (Quick Fix)

### Step 1: Update Google Drive File Permissions
For each of your 15 model files:

1. **Go to Google Drive** → Find your file
2. **Right-click** → **Share**
3. **Change permissions** to:
   - ✅ **"Anyone with the link"**
   - ✅ **"Viewer"** (not Editor)
4. **Copy the sharing link** (should look like: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`)

### Step 2: Update model_config.json
Replace your current URLs with the new sharing links:

```json
{
  "model_urls": {
    "Level1/Fold1": "https://drive.google.com/file/d/135Bantj4cToGl5e7d5pfJg1VDN1B2Rkq/view?usp=sharing",
    "Level1/Fold2": "https://drive.google.com/file/d/1kpPEG9yM6QEEa_bpfWiQHAkcqKUqfZC9/view?usp=sharing",
    // ... update all 15 files
  }
}
```

### Step 3: Use Enhanced Download Script
Replace your current `download_models.py` with the enhanced version that handles:
- ✅ Permission issues
- ✅ Large file confirmations
- ✅ Retry logic
- ✅ Progress indicators
- ✅ Fallback methods

## 🔧 Solution 2: Alternative Download Methods

### Option A: Direct Download URLs
Convert your Google Drive links to direct download format:

```bash
# Original sharing link:
https://drive.google.com/file/d/FILE_ID/view?usp=sharing

# Convert to direct download:
https://drive.google.com/uc?export=download&id=FILE_ID
```

### Option B: Use Alternative Hosting
Consider moving your models to:
- **GitHub Releases** (up to 2GB per file)
- **Hugging Face Hub** (unlimited, free)
- **AWS S3** (pay-per-use)
- **Dropbox** (better API)

## 🚀 Solution 3: Long-term Fix - Hugging Face Hub

### Step 1: Upload Models to Hugging Face
```bash
# Install huggingface_hub
pip install huggingface_hub

# Login to Hugging Face
huggingface-cli login

# Upload your models
huggingface-cli upload your-username/cryptoq-models ./models/
```

### Step 2: Update Download Script
```python
from huggingface_hub import hf_hub_download

def download_from_huggingface():
    models = {
        "Level1/Fold1": "your-username/cryptoq-models",
        "Level1/Fold2": "your-username/cryptoq-models",
        # ... etc
    }
    
    for path, repo_id in models.items():
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=f"{path}/model.pth",
            local_dir="./models/"
        )
```

## 📁 Complete File Structure

```
CryptoQ/
├── download_models_enhanced.py    # Enhanced Python script
├── download_models.sh             # Bash script alternative
├── model_config.json              # Updated with proper URLs
├── requirements.txt               # Updated with requests
├── render.yaml                    # Updated build command
└── models/                        # Downloaded models
    ├── Level1/
    │   ├── Fold1/model.pth
    │   ├── Fold2/model.pth
    │   └── ...
    ├── Level2/
    └── Level3/
```

## 🔄 Updated Requirements.txt

Add these dependencies:
```
requests>=2.25.1
urllib3>=1.26.0
```

## 🚀 Updated Render Configuration

### render.yaml
```yaml
services:
  - type: web
    name: CryptoQ
    env: python
    buildCommand: "pip install -r requirements.txt && python download_models_enhanced.py"
    startCommand: "cd CryptoQWeb && python manage.py runserver 0.0.0.0:$PORT"
    rootDir: .
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: CryptoQWeb.settings
      - key: PYTHONPATH
        value: /opt/render/project/src/CryptoQWeb
```

## 🧪 Testing Locally

### Test the enhanced script:
```bash
# Make script executable
chmod +x download_models.sh

# Run Python version
python download_models_enhanced.py

# Or run Bash version
./download_models.sh
```

### Expected output:
```
Starting CryptoQ Model Download Process...
============================================================
SUCCESS: Directory structure created successfully!

[1/15] Processing Level1/Fold1...
DOWNLOADING Level1/Fold1 (attempt 1/3)...
  Progress: 100.0% (567,234,567/567,234,567 bytes)
SUCCESS: Downloaded Level1/Fold1 (567,234,567 bytes)
----------------------------------------
...
```

## 🚨 Troubleshooting

### Common Issues:

1. **"Access denied"**
   - ✅ Fix: Set Google Drive files to "Anyone with the link"

2. **"File is empty"**
   - ✅ Fix: Use enhanced script with confirmation token handling

3. **"Timeout"**
   - ✅ Fix: Increase timeout in script (already set to 30 minutes)

4. **"Rate limited"**
   - ✅ Fix: Script includes retry logic with delays

### Debug Commands:
```bash
# Test single file download
curl -L "https://drive.google.com/uc?export=download&id=135Bantj4cToGl5e7d5pfJg1VDN1B2Rkq" -o test.pth

# Check file permissions
ls -la models/Level1/Fold1/

# Verify file integrity
file models/Level1/Fold1/model.pth
```

## 📊 Performance Comparison

| Method | Speed | Reliability | Setup |
|--------|-------|-------------|-------|
| Google Drive (Fixed) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Hugging Face Hub | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| GitHub Releases | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| AWS S3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |

## 🎯 Recommended Action Plan

1. **Immediate Fix**: Update Google Drive permissions + use enhanced script
2. **Short-term**: Test deployment on Render
3. **Long-term**: Migrate to Hugging Face Hub for better reliability

## 📞 Support

If you encounter issues:
1. Check Google Drive file permissions
2. Verify file IDs in model_config.json
3. Test locally before deploying
4. Check Render build logs for specific errors
