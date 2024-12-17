from fastapi import APIRouter
from .endpoints import uploads

router = APIRouter()

router.include_router(uploads.router, prefix="/uploads", tags=["File Uploads"]) 