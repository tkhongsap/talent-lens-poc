from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict
from datetime import date


class ContactInfo(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    address: Optional[str] = None


class DateRange(BaseModel):
    start: str  # YYYY-MM format
    end: Optional[str] = None  # YYYY-MM format or "Present"


class WorkExperience(BaseModel):
    job_title: str
    company: str
    dates: DateRange
    responsibilities: List[str]


class Education(BaseModel):
    degree: Optional[str] = None
    major: str
    institution: str
    graduation_date: str  # YYYY-MM format


class AdditionalInfo(BaseModel):
    projects: Optional[List[str]] = None
    awards: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    volunteer: Optional[List[str]] = None


class ResumeOutput(BaseModel):
    contact_info: ContactInfo
    summary: str
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    additional_info: Optional[AdditionalInfo] = None