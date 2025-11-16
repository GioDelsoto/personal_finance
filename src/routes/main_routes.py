from whatsapp_routes import router as whatsapp_router
from fastapi import FastAPI, APIRouter


router = APIRouter()

router.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])
