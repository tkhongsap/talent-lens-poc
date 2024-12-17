import json
from typing import Optional, List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from os import environ
from .resume_schema import RESUME_JSON_SCHEMA

# Load environment variables
load_dotenv()

# Get model from environment or use default
llm_model = environ.get("OPENAI_MODEL", "gpt-4-1106-preview")

# Pydantic models for structured output
class DateRange(BaseModel):
    start: str = Field(description="Start date in YYYY-MM format")
    end: Optional[str] = Field(description="End date in YYYY-MM format or 'Present'")

class WorkExperience(BaseModel):
    job_title: str
    company: str
    dates: DateRange
    responsibilities: List[str]

class Education(BaseModel):
    degree: str
    major: Optional[str]
    institution: str
    graduation_date: str = Field(description="Date in YYYY-MM format")

class ContactInfo(BaseModel):
    name: str
    phone: Optional[str] = Field(pattern=r"^\+?[0-9()-.\s]{10,}$")
    email: Optional[str] = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    linkedin: Optional[str] = Field(pattern=r"^https?://([a-z]{2,3}\.)?linkedin\.com/.*$")
    address: Optional[str]

class AdditionalInfo(BaseModel):
    projects: Optional[List[str]] = []
    awards: Optional[List[str]] = []
    publications: Optional[List[str]] = []
    volunteer: Optional[List[str]] = []

class ResumeOutput(BaseModel):
    contact_info: ContactInfo
    summary: str
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    additional_info: Optional[AdditionalInfo] = Field(default_factory=lambda: AdditionalInfo())

class ResumeJSONConverter:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=api_key)
        
    def convert_to_json(self, markdown_content: str) -> Optional[dict]:
        """Convert markdown resume content to structured JSON format"""
        
        try:
            # Validate API key is set
            if not self.client.api_key:
                raise ValueError("OpenAI API key is not set")

            completion = self.client.chat.completions.create(
                model=llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a precise resume parser that converts markdown-formatted resumes into structured JSON.
Follow these rules strictly:
1. Extract all information exactly as presented
2. Format dates as YYYY-MM
3. Use null for missing optional fields
4. Ensure all arrays are properly formatted
5. Be consistent with date ranges, using "Present" for current positions
6. Split responsibilities into clear, separate items
7. Normalize skill names (e.g., "JavaScript" not "Javascript")"""
                    },
                    {
                        "role": "user",
                        "content": f"Convert this resume to JSON format:\n\n{markdown_content}"
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                seed=42
            )
            
            # Parse the response using Pydantic model
            json_response = json.loads(completion.choices[0].message.content)
            resume = ResumeOutput.model_validate(json_response)
            
            # Convert Pydantic model to dict
            return resume.model_dump(exclude_none=True)
            
        except Exception as e:
            print(f"Error converting resume to JSON: {str(e)}")
            return None

    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date string format (YYYY-MM)"""
        if date_str.lower() == "present":
            return True
        try:
            year, month = date_str.split("-")
            return len(year) == 4 and len(month) == 2 and 1 <= int(month) <= 12
        except:
            return False