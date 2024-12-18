from fastapi import APIRouter
from .endpoints import analysis, uploads

api_router = APIRouter()

# Analysis endpoints
api_router.include_router(
    analysis.router, 
    prefix="/analyze", 
    tags=["Analysis"]
)

# Upload endpoints
api_router.include_router(
    uploads.router, 
    prefix="/uploads", 
    tags=["Uploads"]
) 