from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/environment", tags=["Environment"])
@router.get("/metrics")
def env_metrics():
    return {"temperature": "nominal", "humidity": "nominal"}