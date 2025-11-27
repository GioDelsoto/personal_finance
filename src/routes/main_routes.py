from fastapi import APIRouter
from src.routes.whatsapp_routes import router as whatsapp_router


router = APIRouter()

router.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])
