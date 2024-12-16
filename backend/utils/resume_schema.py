from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field

class DateRange(BaseModel):
    start: str
    end: str

class WorkExperience(BaseModel):
    job_title: str
    company: str
    dates: DateRange
    responsibilities: List[str]

class Education(BaseModel):
    degree: Optional[str] = None
    major: str
    institution: str
    graduation_date: str

class ContactInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    address: Optional[str] = None

class AdditionalInfo(BaseModel):
    projects: Optional[List[str]] = None
    awards: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    volunteer: Optional[List[str]] = None

class ResumeOutput(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str] = None
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    additional_info: Optional[AdditionalInfo] = None