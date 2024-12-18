from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from typing import List, Dict
from app.core.config import get_settings
from app.services.resume_processor import resume_processor
import os
import uuid
import shutil

router = APIRouter()
settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

ALLOWED_JOB_DESC_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

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
    try:
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Validate file extension
        if file_ext not in ALLOWED_JOB_DESC_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_JOB_DESC_EXTENSIONS)}"
            )
        
        # Create unique filename
        unique_filename = f"job_desc_{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "id": unique_filename,
            "filename": file.filename,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job-description/text")
async def create_job_description_from_text(text_data: Dict[str, str] = Body(...)):
    try:
        job_text = text_data.get("text")
        if not job_text:
            raise HTTPException(status_code=400, detail="Job description text is required")
        
        # Create unique filename for the text content
        unique_filename = f"job_desc_{uuid.uuid4()}.txt"
        file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
        
        # Save the text content to a file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(job_text)
            
        return {
            "id": unique_filename,
            "filename": "job_description.txt",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 