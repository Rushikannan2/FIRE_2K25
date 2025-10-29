import os
from huggingface_hub import hf_hub_download

token = os.getenv("HF_TOKEN")
repo = "rushikannan/FIRE_CryptoQA"

levels = ["Level1", "Level2", "Level3"]
folds = ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]

print("Starting CryptoQ Model Download Process...")
print("=" * 60)
success = 0

for level in levels:
    for fold in folds:
        path = f"{level}/{fold}/model.pth"
        try:
            print(f"Downloading {path} ...")
            hf_hub_download(
                repo_id=repo,
                filename=path,
                token=token,
                local_dir=f"models/{level}/{fold}",
            )
            print(f"✅ SUCCESS: {path}")
            success += 1
        except Exception as e:
            print(f"❌ FAILED: {path} — {e}")

print("=" * 60)
print(f"📊 DOWNLOAD SUMMARY\nTotal models: 15\nSuccessful: {success}\nFailed: {15-success}")
print("🎉 All models downloaded successfully!")