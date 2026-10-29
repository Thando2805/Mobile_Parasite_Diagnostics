import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import ParasiteDataset, get_microscopy_transforms
from model import ParasiteClassifier

def train_model():
    train_dir = "data/processed/train"
    val_dir = "data/processed/val"
    save_path = "app/models_weights/parasite_model.pt"
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load datasets
    train_dataset = ParasiteDataset(data_dir=train_dir, transform=get_microscopy_transforms(is_train=True))
    val_dataset = ParasiteDataset(data_dir=val_dir, transform=get_microscopy_transforms(is_train=False))

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)

    num_classes = len(train_dataset.classes)
    model = ParasiteClassifier(num_classes=num_classes).to(device)

    # Loss & Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.5)

    num_epochs = 20
    best_val_acc = 0.0

    print("\n--- Starting Training Loop ---")
    for epoch in range(num_epochs):
        model.train()
        train_loss, train_correct, total_train = 0.0, 0, 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data)
            total_train += images.size(0)

        epoch_train_loss = train_loss / total_train
        epoch_train_acc = train_correct.double() / total_train

        # Validation phase
        model.eval()
        val_loss, val_correct, total_val = 0.0, 0, 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)
                total_val += images.size(0)

        epoch_val_loss = val_loss / total_val
        epoch_val_acc = val_correct.double() / total_val

        scheduler.step(epoch_val_loss)

        print(f"Epoch {epoch+1:02d}/{num_epochs:02d} | "
              f"Train Loss: {epoch_train_loss:.4f} Acc: {epoch_train_acc:.4f} | "
              f"Val Loss: {epoch_val_loss:.4f} Acc: {epoch_val_acc:.4f}")

        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            torch.save(model.state_dict(), save_path)
            print(f"✅ Saved new best model to {save_path} (Val Acc: {best_val_acc:.4f})")

if __name__ == "__main__":
    train_model()