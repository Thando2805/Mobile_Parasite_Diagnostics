import os
import shutil
import random
from pathlib import Path
from datasets import load_dataset
from PIL import Image

def download_and_split_helminths():
    print("🚀 Downloading curated Helminth Egg dataset (~600 MB) from Hugging Face...")
    
    # Load dataset
    ds = load_dataset("Abdelkareem/parasitic-egg")
    
    target_train_dir = Path("data/processed/train")
    target_val_dir = Path("data/processed/val")

    # Map label indices to clean folder names
    labels = ds['train'].features['label'].names
    label_map = {i: name.lower().replace(" ", "_").replace(".", "") for i, name in enumerate(labels)}

    print(f"📌 Found {len(labels)} internal parasite classes:")
    for idx, name in label_map.items():
        print(f"   - [{idx}] {name}")
        (target_train_dir / name).mkdir(parents=True, exist_ok=True)
        (target_val_dir / name).mkdir(parents=True, exist_ok=True)

    print("\n🔄 Sorting and performing 80% train / 20% validation split...")
    
    # Process train split from HF dataset and split into train/val locally
    counts = {name: {"train": 0, "val": 0} for name in label_map.values()}

    # Group records by category
    records_by_class = {idx: [] for idx in label_map.keys()}
    for item in ds['train']:
        records_by_class[item['label']].append(item)

    for cls_idx, items in records_by_class.items():
        cls_name = label_map[cls_idx]
        random.shuffle(items)

        # 80/20 split
        split_point = int(len(items) * 0.8)
        train_items = items[:split_point]
        val_items = items[split_point:]

        # Save train images
        for i, item in enumerate(train_items):
            img = item['image']
            img.save(target_train_dir / cls_name / f"{cls_name}_{i+1}.jpg")
            counts[cls_name]["train"] += 1

        # Save validation images
        for i, item in enumerate(val_items):
            img = item['image']
            img.save(target_val_dir / cls_name / f"{cls_name}_{i+1}.jpg")
            counts[cls_name]["val"] += 1

        print(f"   -> Class '{cls_name}': {counts[cls_name]['train']} train, {counts[cls_name]['val']} val")

    print("\n🎉 Internal parasite dataset successfully organized in `data/processed/`!")
    print("👉 Ready to run training: `python training/train.py`")

if __name__ == "__main__":
    download_and_split_helminths()