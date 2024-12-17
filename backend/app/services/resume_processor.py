import spacy
from typing import Dict, List, Optional
import os
import magic
from ..core.config import get_settings

settings = get_settings()

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class ResumeProcessor:
    def __init__(self):
        self.allowed_mime_types = {
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
        }

    def validate_file(self, file_path: str) -> bool:
        """Validate if the file is of allowed type."""
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        return file_mime in self.allowed_mime_types

    async def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from resume file."""
        # TODO: Implement text extraction based on file type
        # This is a placeholder - you'll need to implement actual extraction
        # using libraries like python-docx for .docx and PyPDF2 for .pdf
        return ""

    async def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP."""
        doc = nlp(text)
        # This is a basic implementation - you'll want to enhance this
        # with a proper skills database and better extraction logic
        skills = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                skills.append(ent.text)
        return list(set(skills))

    async def extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from text."""
        # TODO: Implement more sophisticated experience extraction
        # This is a placeholder implementation
        return []

    async def extract_education(self, text: str) -> List[Dict]:
        """Extract education information from text."""
        # TODO: Implement more sophisticated education extraction
        # This is a placeholder implementation
        return []

    async def process_resume(self, file_path: str) -> Dict:
        """Process resume and extract all relevant information."""
        if not self.validate_file(file_path):
            raise ValueError("Invalid file type")

        text = await self.extract_text(file_path)
        if not text:
            raise ValueError("Could not extract text from file")

        skills = await self.extract_skills(text)
        experience = await self.extract_experience(text)
        education = await self.extract_education(text)

        return {
            "skills": skills,
            "experience": experience,
            "education": education,
            "raw_text": text
        }


# Create a singleton instance
resume_processor = ResumeProcessor() 