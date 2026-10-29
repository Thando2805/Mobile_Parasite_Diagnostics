import torch
import torch.nn.functional as F
from app.config import settings
from app.services.preprocessor import process_image_bytes
from training.model import ParasiteClassifier

class InferenceService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.model = ParasiteClassifier(num_classes=len(settings.CLASSES))
            state_dict = torch.load(settings.MODEL_PATH, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model successfully loaded on {self.device}")
        except Exception as e:
            print(f"Warning: Could not load model weights from {settings.MODEL_PATH}. Details: {e}")

    def predict(self, image_bytes: bytes):
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        
        tensor = process_image_bytes(image_bytes).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, pred_idx = torch.max(probabilities, dim=1)
            
        class_name = settings.CLASSES[pred_idx.item()]
        return {
            "prediction": class_name,
            "confidence": round(float(confidence.item()) * 100, 2),
            "class_index": pred_idx.item()
        }

inference_service = InferenceService()