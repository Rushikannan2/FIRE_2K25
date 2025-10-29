import os
import sys
from huggingface_hub import hf_hub_download

token = os.getenv("HF_TOKEN")
if not token:
    print("❌ ERROR: HF_TOKEN environment variable not set!")
    sys.exit(1)

repo = "rushikannan/FIRE_CryptoQA"

levels = ["Level1", "Level2", "Level3"]
folds = ["Fold1", "Fold2", "Fold3", "Fold4", "Fold5"]

print("Starting CryptoQ Model Download Process...")
print("=" * 60)
success = 0

for level in levels:
    for fold in folds:
        # Files in HF repo are under models/LevelX/FoldY/model.pth
        path = f"models/{level}/{fold}/model.pth"
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
if success == 15:
    print("🎉 All models downloaded successfully!")
    sys.exit(0)
else:
    print("⚠️ Some models failed to download. Check errors above.")
    sys.exit(1)