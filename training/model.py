import torch
import torch.nn as nn
import torchvision.models as models

def ParasiteClassifier(num_classes=3):
    """
    Loads MobileNetV3 Large matching your checkpoint dimensions 
    (classifier input features 1280, output classes 3).
    """
    # Load MobileNetV3 Large without pretrained weights
    model = models.mobilenet_v3_large(weights=None)
    
    # Your checkpoint shows classifier.0 is Linear(960 -> 1280) or similar large variant structure,
    # and classifier.3 is the final Linear layer. Torchvision's default mobilenet_v3_large 
    # matches this 1280 feature map size.
    
    in_features = model.classifier[3].in_features  # typically 1280
    model.classifier[3] = nn.Linear(in_features, num_classes)
    
    return model