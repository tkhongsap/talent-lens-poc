from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from ....core.config import get_settings
from ....services.resume_processor import resume_processor
import os
import uuid

router = APIRouter()
settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

@router.post("/resume")
async def upload_resumes(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext[1:] not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
        
        # Save file
        try:
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            
            results.append({
                "filename": file.filename,
                "saved_as": unique_filename,
                "file_path": file_path,
                "size": len(contents)
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return {"uploaded_files": results}

@router.post("/job-description")
async def upload_job_description(file: UploadFile = File(...)):
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext[1:] not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Generate unique filename
    unique_filename = f"job_{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
    
    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "filename": file.filename,
            "saved_as": unique_filename,
            "file_path": file_path,
            "size": len(contents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}") 