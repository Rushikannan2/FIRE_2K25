@echo off
echo 🚀 CryptoQ Hugging Face Quick Start
echo ====================================
echo.
echo This will:
echo 1. Install required packages
echo 2. Authenticate with Hugging Face  
echo 3. Upload all your models
echo 4. Test the download
echo.
pause

echo.
echo 📦 Installing packages...
pip install huggingface_hub[cli] requests tqdm

echo.
echo 🔐 Authenticating with Hugging Face...
echo Please follow the browser prompts...
hf auth login

echo.
echo 📤 Uploading models...
python upload_models.py

echo.
echo 📥 Testing download...
python download_models_hf.py

echo.
echo ✅ Setup complete!
echo Your models are now on Hugging Face!
echo Repository: https://huggingface.co/rushikannan/FIRE_CryptoQA
echo.
pause







