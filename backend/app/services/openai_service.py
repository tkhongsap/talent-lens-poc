from openai import OpenAI
from typing import Dict, Any
import json
from ..utils.prompting_instructions import (
    JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT,
    RESUME_PARSER_SYSTEM_PROMPT,
    FIT_SCORE_SYSTEM_PROMPT
)

class OpenAIService:
    def __init__(self, api_key: str, model: str = "gpt-4-1106-preview"):
        if not api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def parse_job_description(self, content: str) -> Dict[str, Any]:
        """Parse job description using standardized prompt"""
        return await self.process_with_prompt(content, JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT)
    
    async def parse_resume(self, content: str) -> Dict[str, Any]:
        """Parse resume using standardized prompt"""
        return await self.process_with_prompt(content, RESUME_PARSER_SYSTEM_PROMPT)
    
    async def calculate_fit_score(
        self, 
        resume_json: Dict[str, Any], 
        job_desc_json: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate fit score using standardized prompt"""
        try:
            input_content = {
                "job_description": job_desc_json,
                "resume": resume_json
            }
            
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": FIT_SCORE_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": json.dumps(input_content)
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Error calculating fit score: {str(e)}")
    
    async def process_with_prompt(self, content: str, system_prompt: str) -> Dict[str, Any]:
        """
        Process content with OpenAI using a specific system prompt
        
        Args:
            content (str): Content to process
            system_prompt (str): System prompt to use
            
        Returns:
            Dict[str, Any]: Processed JSON response
        """
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Parse this content into structured JSON:\n\n{content}"
                    }
                ],
                temperature=0.3,
                seed=42
            )
            
            # Parse the response
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Error processing with OpenAI: {str(e)}")