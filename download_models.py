import os
from huggingface_hub import hf_hub_download

# Load Hugging Face access token from Render environment
token = os.getenv("HF_TOKEN")
repo = "rushikannan/FIRE_CryptoQA"

# Define levels and folds
levels = ["Level1", "Level2", "Level3"]
folds = ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]

print("🔁 Starting CryptoQ Model Download Process...")
print("=" * 60)

for level in levels:
    for fold in folds:
        filename = f"models/{level}/{fold}/model.pth"
        try:
            print(f"⬇️  Downloading {filename} ...")
            hf_hub_download(
                repo_id=repo,
                filename=filename,
                token=token,
                local_dir=f"models/{level}/{fold}",
                local_dir_use_symlinks=False
            )
            print(f"✅ SUCCESS: {filename}")
        except Exception as e:
            print(f"❌ FAILED: {filename} — {e}")

print("=" * 60)
print("✅ All available models processed successfully.")