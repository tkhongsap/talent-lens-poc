from fastapi import APIRouter, UploadFile, Form
from app.services.parser_service import ParserService

router = APIRouter()
parser_service = ParserService()

@router.get("/")
async def analysis_root():
    return {"message": "Analysis endpoint operational"}

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile,
    job_description: str = Form(...)
):
    # Parse resume
    resume_content = await resume.read()
    resume_data = await parser_service.parse_document(resume_content, is_resume=True)
    
    # Parse job description
    job_data = await parser_service.parse_document(
        job_description.encode(), 
        is_resume=False
    )
    
    return {
        "resumeInfo": resume_data,
        "jobInfo": job_data
    } 