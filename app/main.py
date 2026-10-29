import os
import io
import numpy as np
from PIL import Image
import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Parasite Diagnostic API", version="2.0")

# Enable CORS for frontend and mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Comprehensive scientific label mappings across all 4 specialized models
PARASITE_LABELS = {
    "malaria": {
        0: "Negative / No Parasites Detected",
        1: "Plasmodium falciparum (Malaria Parasite)"
    },
    "environmental": {
        0: "Clean Water / Uncontaminated",
        1: "Giardia lamblia (Cyst)",
        2: "Cryptosporidium parvum (Oocyst)"
    },
    "external_parasite": {
        0: "Normal Skin / Negative",
        1: "Ixodidae (Hard Tick)",
        2: "Sarcoptes scabiei (Mite)",
        3: "Pediculus humanus (Head Louse)",
        4: "Cimex lectularius (Bed Bug)",
        5: "Pulex irritans (Human Flea)",
        6: "Demodex folliculorum (Follicle Mite)",
        7: "Argasidae (Soft Tick)"
    },
    "helminth": {
        0: "Negative / Clear Sample",
        1: "Ascaris lumbricoides (Roundworm Egg)",
        2: "Ancylostoma duodenale (Hookworm Egg)", # <--- Endoparasite / Intestinal Worm
        3: "Trichuris trichiura (Whipworm Egg)",
        4: "Enterobius vermicularis (Pinworm Egg)",
        5: "Schistosoma mansoni (Blood Fluke Egg)",
        6: "Schistosoma haematobium Egg",
        7: "Taenia spp. (Tapeworm Egg)",
        8: "Fasciola hepatica (Liver Fluke Egg)",
        9: "Strongyloides stercoralis (Larva)",
        10: "Clonorchis sinensis Egg"
    }
}

# Map incoming domain names from frontend to filename prefixes
MODEL_MAPPING = {
    "Malaria": "malaria_best",
    "External Parasites": "external_parasite_best",
    "Helminths": "helminth_best",
    "Environmental & Waterborne Pathogens": "environmental_parasite_best"
}

# Cache for loaded ONNX sessions to optimize inference speed
onnx_sessions = {}

def get_onnx_session(domain_key: str):
    if domain_key not in onnx_sessions:
        filename = f"{MODEL_MAPPING[domain_key]}.onnx"
        weights_path = os.path.join("app", "models_weights", filename)
        if not os.path.exists(weights_path):
            raise HTTPException(status_code=500, detail=f"ONNX model file not found at {weights_path}")
        onnx_sessions[domain_key] = ort.InferenceSession(weights_path)
    return onnx_sessions[domain_key]

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # Standard ImageNet normalization matching training pipeline
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img_array = (img_array - mean) / std
        
        # Reshape [H, W, C] to [C, H, W] and add batch dimension [1, C, H, W]
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=-1, keepdims=True)

@app.get("/")
def read_root():
    return {"message": "Parasite Diagnostic ONNX API is online and operational!"}

@app.post("/api/v1/predict")
async def predict_parasite(
    file: UploadFile = File(...),
    domain: str = Form("Malaria")
):
    if domain not in MODEL_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid diagnostic domain selected.")
    
    contents = await file.read()
    input_tensor = preprocess_image(contents)
    
    session = get_onnx_session(domain)
    input_name = session.get_inputs()[0].name
    
    # Run ONNX inference
    raw_output = session.run(None, {input_name: input_tensor})[0]
    probabilities = softmax(raw_output[0])
    
    predicted_index = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_index])
    
    # Map domain to dictionary key prefix
    dict_key_map = {
        "Malaria": "malaria",
        "External Parasites": "external_parasite",
        "Helminths": "helminth",
        "Environmental & Waterborne Pathogens": "environmental"
    }
    
    label_dict = PARASITE_LABELS[dict_key_map[domain]]
    parasite_name = label_dict.get(predicted_index, f"Pathogen Class {predicted_index}")
    
    return {
        "domain": domain,
        "predicted_class_index": predicted_index,
        "parasite_name": parasite_name,
        "confidence": confidence,
        "all_probabilities": {label_dict.get(i, f"Class {i}"): float(p) for i, p in enumerate(probabilities)}
    }