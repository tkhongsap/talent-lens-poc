from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from pydantic import BaseModel
import logging
import traceback
from app.services.storage_service import StorageService
from io import BytesIO

router = APIRouter()
logger = logging.getLogger(__name__)
storage_service = StorageService()

class JobDescriptionText(BaseModel):
    text: str

@router.post("/job-description")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload a job description file"""
    try:
        # Store file
        file_id = await storage_service.store_file(file)
        logger.info(f"File stored with ID: {file_id}")
        return {"file_id": file_id}
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a single resume file"""
    try:
        logger.info(f"Received resume upload request: {file.filename}, {file.content_type}")
        file_id = await storage_service.store_file(file)
        logger.info(f"Stored resume file: {file_id}")
        return {"file_id": file_id}
    except Exception as e:
        logger.error(f"Error in upload_resume: {str(e)}")
        logger.error(f"Full error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=422, 
            detail={"error": str(e), "type": "resume_upload_error"}
        )

@router.post("/job-description-text")
async def upload_job_description_text(job_desc: JobDescriptionText):
    """Upload job description as text"""
    try:
        # Create a text file in memory
        file_content = BytesIO(job_desc.text.encode())
        file = UploadFile(
            file=file_content,
            filename="job_description.txt"
        )
        
        # Store file and get ID
        file_id = await storage_service.store_file(file)
        logger.info(f"Stored job description text as file: {file_id}")
        return {"file_id": file_id}
    except Exception as e:
        logger.error(f"Error in upload_job_description_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/debug/storage/{file_id}")
async def debug_storage(file_id: str):
    """Debug endpoint to check storage content"""
    try:
        stored_data = storage_service._files.get(file_id)
        return {
            "exists": file_id in storage_service._files,
            "type": str(type(stored_data)),
            "is_tuple": isinstance(stored_data, tuple),
            "length": len(stored_data) if isinstance(stored_data, tuple) else None,
            "filename": stored_data[0] if isinstance(stored_data, tuple) else None,
            "content_length": len(stored_data[1]) if isinstance(stored_data, tuple) else None
        }
    except Exception as e:
        return {"error": str(e)} 