from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from llama_parse import LlamaParse
from openai import AsyncOpenAI
import os
from app.core.config import get_settings
import json
import asyncio
import nest_asyncio
import sys
from app.services.parser_service import ParserService
from app.services.storage_service import StorageService
from app.services.analysis_service import AnalysisService

# Add debug logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Apply nest_asyncio and log the result
try:
    nest_asyncio.apply()
    logger.info("nest_asyncio applied successfully")
except Exception as e:
    logger.error(f"Failed to apply nest_asyncio: {str(e)}")
    raise

router = APIRouter()
settings = get_settings()
storage_service = StorageService()

class AnalysisRequest(BaseModel):
    resume_id: str
    job_description_id: str

class ParsedContent(BaseModel):
    original_text: str
    markdown_content: str
    structured_data: dict

class AnalysisResponse(BaseModel):
    resumeId: str
    fileName: str
    parsed_resume: ParsedContent
    parsed_job_description: ParsedContent
    analysis_results: dict

@router.post("/", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest):
    logger.info(f"Analysis request received for resume_id: {request.resume_id} and job_description_id: {request.job_description_id}")
    
    # Validate file IDs exist before proceeding
    try:
        # Check if files exist in storage - use _files instead of files
        available_files = list(StorageService._files.keys())
        logger.info(f"Available files in storage: {available_files}")
        
        if request.resume_id not in available_files:
            raise HTTPException(
                status_code=404,
                detail=f"Resume file not found. Available files: {available_files}"
            )
            
        if request.job_description_id not in available_files:
            raise HTTPException(
                status_code=404,
                detail=f"Job description file not found. Available files: {available_files}"
            )
            
        parser_service = ParserService()
        
        # Get files from storage
        try:
            logger.info(f"Retrieving files from storage...")
            # Get files - each get_file call returns (filename, content)
            resume_data = await storage_service.get_file(request.resume_id)
            logger.info(f"Retrieved resume file: {resume_data[0]}")
            
            job_desc_data = await storage_service.get_file(request.job_description_id)
            logger.info(f"Retrieved job description file: {job_desc_data[0]}")
            
        except FileNotFoundError as e:
            logger.error(f"File retrieval error: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        
        # Parse both documents
        resume_result = await parser_service.parse_document(resume_data, is_resume=True)
        job_desc_result = await parser_service.parse_document(job_desc_data, is_resume=False)
        
        analysis_service = AnalysisService()
        
        # Calculate matches
        skills_match, missing_skills = analysis_service.calculate_skills_match(
            resume_result['structured_data']['skills'],
            job_desc_result['structured_data']['qualifications']
        )
        
        experience_match, experience_gaps = analysis_service.calculate_experience_match(
            resume_result['structured_data'],
            job_desc_result['structured_data']
        )
        
        education_match, education_recommendations = analysis_service.calculate_education_match(
            resume_result['structured_data'],
            job_desc_result['structured_data']
        )
        
        overall_match = analysis_service.calculate_overall_match(
            skills_match,
            experience_match,
            education_match
        )
        
        # Compile recommendations
        recommendations = []
        if missing_skills:
            recommendations.append(f"Consider developing skills in: {', '.join(missing_skills)}")
        recommendations.extend(education_recommendations)
        if experience_gaps:
            recommendations.extend(experience_gaps)

        analysis = {
            "skillsMatch": skills_match,
            "experienceMatch": experience_match,
            "educationMatch": education_match,
            "overallFit": overall_match,
            "recommendations": recommendations
        }
        
        # Optionally, clean up files from memory if desired
        await storage_service.cleanup_file(request.resume_id)
        await storage_service.cleanup_file(request.job_description_id)

        return {
            "resumeId": request.resume_id,
            "fileName": resume_data[0],
            "parsed_resume": {
                "original_text": resume_result['markdown_content'],
                "markdown_content": resume_result['markdown_content'],
                "structured_data": resume_result['structured_data']
            },
            "parsed_job_description": {
                "original_text": job_desc_result['markdown_content'],
                "markdown_content": job_desc_result['markdown_content'],
                "structured_data": job_desc_result['structured_data']
            },
            "analysis_results": analysis
        }

    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 