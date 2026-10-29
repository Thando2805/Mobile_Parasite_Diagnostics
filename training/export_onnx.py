import os
import sys
import torch

# Ensure root directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from training.model import ParasiteClassifier

# List of all 4 trained model weight files
MODEL_FILES = [
    "environmental_parasite_best.pth",
    "external_parasite_best.pth",
    "helminth_best.pth",
    "malaria_best.pth"
]

def export_all_to_onnx():
    device = torch.device("cpu")
    weights_dir = "app/models_weights"
    
    dummy_input = torch.randn(1, 3, 224, 224, device=device)

    for model_file in MODEL_FILES:
        weights_path = os.path.join(weights_dir, model_file)
        
        if not os.path.exists(weights_path):
            print(f"Skipping {model_file}: File not found at {weights_path}")
            continue
            
        print(f"\nLoading checkpoint for {model_file}...")
        state_dict = torch.load(weights_path, map_location=device)
        
        # Dynamically determine the number of output classes from the checkpoint weights
        if "classifier.3.weight" in state_dict:
            num_classes = state_dict["classifier.3.weight"].shape[0]
        else:
            num_classes = 2  # fallback default
            
        print(f"-> Detected {num_classes} classes for {model_file}. Initializing architecture...")
        model = ParasiteClassifier(num_classes=num_classes)
        
        model.load_state_dict(state_dict)
        model.eval()
        
        onnx_output_path = weights_path.replace(".pth", ".onnx")
        
        print(f"-> Exporting to ONNX -> {onnx_output_path}")
        torch.onnx.export(
            model,
            dummy_input,
            onnx_output_path,
            export_params=True,
            opset_version=12,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={
                "input": {0: "batch_size"},
                "output": {0: "batch_size"}
            }
        )
        print(f"Successfully exported {model_file}!")

    print("\nAll available models exported to ONNX successfully!")

if __name__ == "__main__":
    export_all_to_onnx()