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
    try:
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
        
        # Use OpenAI to analyze the parsed content
        try:
            analysis_response = await parser_service.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume analyzer."},
                    {"role": "user", "content": f"""
                    Compare this resume with the job description and provide analysis:
                    
                    RESUME:
                    {resume_result['markdown_content']}
                    
                    JOB DESCRIPTION:
                    {job_desc_result['markdown_content']}
                    
                    Provide a detailed analysis including skills match, experience match, 
                    education match, overall fit, and specific recommendations.
                    """}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(analysis_response.choices[0].message.content)
            logger.info("Analysis completed successfully")
            
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {str(e)}")
            # Fallback to mock data if OpenAI fails
            analysis = {
                "skillsMatch": 80.0,
                "experienceMatch": 85.0,
                "educationMatch": 90.0,
                "overallFit": 85.5,
                "recommendations": [
                    "Consider highlighting your project management experience",
                    "Add more details about your technical skills",
                    "Include certifications if available"
                ]
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