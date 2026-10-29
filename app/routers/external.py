from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.inference import inference_service

router = APIRouter(prefix="/api/v1", tags=["External Inference"])

@router.post("/predict")
async def predict_parasite(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not a valid image.")
    try:
        image_bytes = await file.read()
        result = inference_service.predict(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))