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