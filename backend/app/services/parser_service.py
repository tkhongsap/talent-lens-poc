from llama_parse import LlamaParse
from openai import OpenAI
from ..core.config import get_settings
from ..utils.prompting_instructions import (
    JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT,
    RESUME_PARSER_SYSTEM_PROMPT
)
import json

settings = get_settings()

class ParserService:
    def __init__(self):
        self.llama_parser = LlamaParse(api_key=settings.LLAMA_CLOUD_API_KEY)
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def parse_document(self, content: bytes, is_resume: bool = True):
        """Parse document content using LlamaParse and OpenAI"""
        # First pass: Convert to markdown using LlamaParse
        markdown_content = self.llama_parser.parse_document(content)

        # Second pass: Structure the content using OpenAI
        system_prompt = RESUME_PARSER_SYSTEM_PROMPT if is_resume else JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT
        
        completion = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": markdown_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return json.loads(completion.choices[0].message.content) 