from fastapi import APIRouter, HTTPException
from typing import Dict, List
import os
from ....services.resume_processor import resume_processor
from ....services.job_processor import job_processor
from ....services.fit_score import calculate_fit_score
from ....core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/analyze")
async def analyze_resume(data: Dict):
    try:
        resume_id = data.get("resumeId")
        job_description_id = data.get("jobDescriptionId")
        
        # Get processed resume data
        resume_data = await resume_processor.get_processed_resume(resume_id)
        if not resume_data:
            raise HTTPException(status_code=404, detail="Resume not found")
            
        # Get processed job description
        job_data = await job_processor.get_processed_job(job_description_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job description not found")
            
        # Calculate fit score
        fit_score = await calculate_fit_score(resume_data, job_data)
        
        return {
            "resumeId": resume_id,
            "fileName": resume_data.get("original_filename", "Unknown"),
            "score": fit_score.get("overall_score", 0),
            "details": {
                "skillsMatch": fit_score.get("skills_match", 0),
                "experienceMatch": fit_score.get("experience_match", 0),
                "educationMatch": fit_score.get("education_match", 0),
                "overallFit": fit_score.get("overall_score", 0),
                "recommendations": fit_score.get("recommendations", [])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 