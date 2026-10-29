import io
from PIL import Image
import torch
from torchvision import transforms

def get_inference_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225]
        )
    ])

def process_image_bytes(image_bytes: bytes) -> torch.Tensor:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    transform = get_inference_transforms()
    tensor = transform(image).unsqueeze(0)  # Adds batch dimension -> [1, 3, 224, 224]
    return tensor