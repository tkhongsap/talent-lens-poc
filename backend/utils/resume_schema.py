from typing import List, Optional
from pydantic import BaseModel, Field, validator

class DateRange(BaseModel):
    start: str = Field(description="Start date in YYYY-MM format")
    end: Optional[str] = Field(description="End date in YYYY-MM format or 'Present'")

class WorkExperience(BaseModel):
    job_title: str
    company: str
    dates: DateRange
    responsibilities: List[str]

class Education(BaseModel):
    degree: Optional[str]
    major: str
    institution: str
    graduation_date: str = Field(description="Date in YYYY-MM format")

class ContactInfo(BaseModel):
    name: str
    phone: Optional[str] = Field(pattern=r"^\+?[0-9()-.\s]{10,}$")
    email: Optional[str] = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    linkedin: Optional[str] = Field(pattern=r"^(?:https?:\/\/)?(?:[a-z]{2,3}\.)?linkedin\.com\/.*$")
    address: Optional[str]

    @validator('linkedin')
    def ensure_linkedin_https(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v

class ResumeOutput(BaseModel):
    contact_info: ContactInfo
    summary: str
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    additional_info: Optional[dict] = None