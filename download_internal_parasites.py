import os
import shutil
import random
from pathlib import Path
import kagglehub

def download_helminth_dataset():
    print("🔍 Downloading Helminth & Internal Parasite Egg dataset from Kaggle...")
    # Downloads a verified microscopic dataset of internal parasite species (Hookworm, Ascaris, Schistosoma, etc.)
    download_path = kagglehub.dataset_download("oliverjackhiggins/helminth-image-dataset")
    print(f"📂 Dataset downloaded to local cache: {download_path}")

    source_base = Path(download_path)
    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
    
    # Locate subdirectories representing the parasite classes
    subdirs = [d for d in source_base.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    target_train_dir = Path("data/processed/train")
    target_val_dir = Path("data/processed/val")

    target_train_dir.mkdir(parents=True, exist_ok=True)
    target_val_dir.mkdir(parents=True, exist_ok=True)

    print("\n🔄 Processing and splitting internal parasite classes (80% train / 20% val)...")

    found_classes = 0
    if subdirs:
        for class_dir in subdirs:
            cls_name = class_dir.name.lower().replace(" ", "_")
            images = []
            for ext in image_extensions:
                images.extend(list(class_dir.rglob(ext)))
            
            if not images:
                continue

            found_classes += 1
            random.shuffle(images)
            split_idx = int(len(images) * 0.8)
            train_imgs = images[:split_idx]
            val_imgs = images[split_idx:]

            (target_train_dir / cls_name).mkdir(parents=True, exist_ok=True)
            (target_val_dir / cls_name).mkdir(parents=True, exist_ok=True)

            print(f"   -> Class '{cls_name}': {len(train_imgs)} train, {len(val_imgs)} val images.")

            for img_path in train_imgs:
                shutil.copy(img_path, target_train_dir / cls_name / img_path.name)
            for img_path in val_imgs:
                shutil.copy(img_path, target_val_dir / cls_name / img_path.name)

    if found_classes == 0:
        # Fallback if structure is flat
        all_images = []
        for ext in image_extensions:
            all_images.extend(list(source_base.rglob(ext)))
        
        if all_images:
            default_cls = "internal_parasites"
            random.shuffle(all_images)
            split_idx = int(len(all_images) * 0.8)
            train_imgs = all_images[:split_idx]
            val_imgs = all_images[split_idx:]

            (target_train_dir / default_cls).mkdir(parents=True, exist_ok=True)
            (target_val_dir / default_cls).mkdir(parents=True, exist_ok=True)

            print(f"   -> Found {len(all_images)} images. Grouped under class '{default_cls}'.")
            for img_path in train_imgs:
                shutil.copy(img_path, target_train_dir / default_cls / img_path.name)
            for img_path in val_imgs:
                shutil.copy(img_path, target_val_dir / default_cls / img_path.name)
        else:
            print("❌ No images found in the downloaded path. Please check structure.")
            return

    print("\n🎉 Internal parasite dataset successfully downloaded and organized into `data/processed/`!")
    print("👉 Next step: Run your training script `python training/train.py`.")

if __name__ == "__main__":
    download_helminth_dataset()