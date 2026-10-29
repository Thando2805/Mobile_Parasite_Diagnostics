import os

folders = [
    "data/raw",
    "data/processed/train",
    "data/processed/val",
    "training",
    "app/routers",
    "app/services",
    "app/models_weights",
    "tests"
]

files = [
    "training/dataset.py",
    "training/model.py",
    "training/train.py",
    "training/export_onnx.py",
    "app/main.py",
    "app/config.py",
    "app/routers/__init__.py",
    "app/routers/internal.py",
    "app/routers/external.py",
    "app/routers/environmental.py",
    "app/services/inference.py",
    "app/services/preprocessor.py",
    "requirements.txt",
    "Dockerfile",
    ".gitignore",
    "README.md"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created directory: {folder}")

for file_path in files:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass
        print(f"Created file: {file_path}")

print("\nStructure initialized successfully!")