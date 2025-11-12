# CryptoQ Hugging Face Quick Start
Write-Host "🚀 CryptoQ Hugging Face Quick Start" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "1. Install required packages" -ForegroundColor White
Write-Host "2. Authenticate with Hugging Face" -ForegroundColor White  
Write-Host "3. Upload all your models" -ForegroundColor White
Write-Host "4. Test the download" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"

Write-Host ""
Write-Host "📦 Installing packages..." -ForegroundColor Blue
pip install huggingface_hub[cli] requests tqdm

Write-Host ""
Write-Host "🔐 Authenticating with Hugging Face..." -ForegroundColor Blue
Write-Host "Please follow the browser prompts..." -ForegroundColor Yellow
hf auth login

Write-Host ""
Write-Host "📤 Uploading models..." -ForegroundColor Blue
python upload_models.py

Write-Host ""
Write-Host "📥 Testing download..." -ForegroundColor Blue
python download_models_hf.py

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host "Your models are now on Hugging Face!" -ForegroundColor Green
Write-Host "Repository: https://huggingface.co/rushikannan/FIRE_CryptoQA" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"







