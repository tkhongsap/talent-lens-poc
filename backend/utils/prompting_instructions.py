# Resume parsing instruction
RESUME_PARSING_INSTRUCTION = """
The provided document is a resume or CV. Extract the following information and output it as a JSON object with this structure:

{
    "contact_info": {
        "name": "string",
        "phone": "string or null",
        "email": "string or null",
        "linkedin": "string or null",
        "address": "string or null"
    },
    "summary": "string",
    "work_experience": [
        {
            "job_title": "string",
            "company": "string",
            "dates": {
                "start": "YYYY-MM",
                "end": "YYYY-MM or Present"
            },
            "responsibilities": ["string"]
        }
    ],
    "education": [
        {
            "degree": "string",
            "major": "string",
            "institution": "string",
            "graduation_date": "YYYY-MM"
        }
    ],
    "skills": ["string"],
    "additional_info": {
        "projects": ["string"] or null,
        "awards": ["string"] or null,
        "publications": ["string"] or null,
        "volunteer": ["string"] or null
    }
}

Follow these rules strictly:
1. Extract all information exactly as presented
2. Format dates as YYYY-MM
3. Use null for missing optional fields
4. Ensure all arrays are properly formatted
5. Be consistent with date ranges, using "Present" for current positions
6. Split responsibilities into clear, separate items
7. Normalize skill names (e.g., "JavaScript" not "Javascript")
""" 

FIT_SCORE_SYSTEM_PROMPT = """You are an expert HR analyst evaluating job applications. Given a job description and a candidate's resume, provide a comprehensive evaluation in JSON format with the following structure:
{
    "executive_summary": "A brief professional summary of the candidate, highlighting their background and key qualifications",
    
    "fit_analysis": {
        "overall_assessment": "A detailed explanation of why the candidate is or isn't a good fit for the role",
        "fit_score": "Integer (0-100) representing overall fitness for the job"
    },
    
    "key_strengths": {
        "skills": ["Array of relevant skills that align well with the job requirements"],
        "experience": ["Array of relevant experience that directly contributes to the role"],
        "notable_achievements": ["Array of achievements that demonstrate capability for the role"]
    },
    
    "areas_for_development": {
        "skills_gaps": ["Skills mentioned in job description that the candidate might need to develop"],
        "experience_gaps": ["Areas where additional experience would be beneficial"],
        "recommendations": ["Specific recommendations for professional development"]
    },
    
    "score_breakdown": {
        "skills_match": "Score (0-100) with brief explanation",
        "experience_match": "Score (0-100) with brief explanation"
    },
    
    "interesting_fact": "A unique or standout fact about the candidate that might be relevant to the role"
}

Guidelines:
1. Be specific and provide context in your assessments
2. Focus on both technical and professional aspects
3. Be constructive in areas for development
4. Consider both current capabilities and potential
5. Highlight specific examples from the resume when possible
""" 