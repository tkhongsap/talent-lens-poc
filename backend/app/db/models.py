from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}


class ResumeBase(BaseModel):
    title: str
    user_id: PyObjectId
    file_path: str
    file_type: str
    status: str = "pending"  # pending, processed, failed


class ResumeInDB(ResumeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    processed_data: Optional[Dict] = None
    skills: List[str] = []
    experience: List[Dict] = []
    education: List[Dict] = []

    class Config:
        json_encoders = {ObjectId: str}


class JobBase(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    location: str
    job_type: str  # full-time, part-time, contract
    status: str = "active"  # active, closed


class JobInDB(JobBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: PyObjectId
    applicants: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}


class AnalyticsBase(BaseModel):
    user_id: PyObjectId
    event_type: str  # search, view_profile, apply_job, etc.
    event_data: Dict


class AnalyticsInDB(AnalyticsBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str} 