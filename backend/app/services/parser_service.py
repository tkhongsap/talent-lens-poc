from llama_parse import LlamaParse
from openai import AsyncOpenAI
from ..core.config import get_settings, refresh_settings
from ..utils.prompting_instructions import (
    JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT,
    RESUME_PARSER_SYSTEM_PROMPT,
    RESUME_SUMMARIZER_SYSTEM_PROMPT
)
import json
import io
import logging
from typing import Tuple
import os
import traceback

logger = logging.getLogger(__name__)

class ParserService:
    def __init__(self):
        logger.info("Initializing ParserService...")
        
        # Refresh settings to ensure we get latest env vars
        refresh_settings()
        settings = get_settings()
        
        # Debug logging
        logger.info(f"LLAMA_CLOUD_API_KEY from env: {os.getenv('LLAMA_CLOUD_API_KEY')[:10]}...")
        logger.info(f"LLAMA_CLOUD_API_KEY from settings: {settings.LLAMA_CLOUD_API_KEY[:10]}...")
        
        if not settings.LLAMA_CLOUD_API_KEY:
            logger.error("LLAMA_CLOUD_API_KEY is empty or not set")
            raise ValueError("LlamaParse API key not found in settings")
            
        self.llama_parser = LlamaParse(
            api_key=settings.LLAMA_CLOUD_API_KEY.strip(),
            result_type="markdown"
        )
        
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is empty or not set")
            raise ValueError("OpenAI API key not found in settings")
            
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY.strip()
        )
        self.model = settings.OPENAI_MODEL

    async def parse_document(self, file_data: Tuple[str, bytes], is_resume: bool = True) -> dict:
        """Parse document content using LlamaParse and OpenAI"""
        try:
            filename, content = file_data
            logger.info(f"Processing file: {filename}, content size: {len(content)} bytes")
            
            # Create buffer for PDF processing
            buffer = io.BytesIO(content)
            
            try:
                logger.info("Starting LlamaParse extraction...")
                logger.info(f"File type: {filename.split('.')[-1].lower()}")
                
                if filename.lower().endswith('.pdf'):
                    pdf_header = content[:8].hex()
                    logger.info(f"PDF header bytes: {pdf_header}")
                
                # Pass filename in extra_info when using buffer
                documents = self.llama_parser.load_data(
                    buffer,
                    extra_info={"file_name": filename}
                )
                
                if not documents:
                    logger.error("LlamaParse returned empty documents list")
                    raise ValueError("No content extracted from document")
                
                # Log document details
                logger.info(f"Extracted {len(documents)} document sections")
                for i, doc in enumerate(documents):
                    logger.info(f"Section {i+1} length: {len(doc.text)} chars")
                    logger.info(f"Section {i+1} preview: {doc.text[:200]}...")
                
                markdown_content = "\n\n".join([doc.text for doc in documents])
                logger.info(f"Total markdown content length: {len(markdown_content)}")
                
                # Log a preview of the content for debugging
                preview = markdown_content[:200] + "..." if len(markdown_content) > 200 else markdown_content
                logger.info(f"Content preview: {preview}")
                
                # Process with OpenAI
                logger.info("Starting OpenAI processing...")
                system_prompt = RESUME_SUMMARIZER_SYSTEM_PROMPT if is_resume else JOB_DESCRIPTION_PARSER_SYSTEM_PROMPT
                
                try:
                    completion = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Parse this content:\n\n{markdown_content}"}
                        ],
                        temperature=0.3,
                        seed=42
                    )
                    
                    raw_response = completion.choices[0].message.content
                    
                    logger.info("Successfully processed content with OpenAI")
                    
                    return {
                        "filename": filename,
                        "original_text": raw_response,
                        "markdown_content": markdown_content,
                        "structured_data": {}
                    }
                    
                except Exception as e:
                    logger.error(f"OpenAI processing failed: {str(e)}")
                    raise
                    
            except Exception as e:
                logger.error(f"LlamaParse extraction failed: {str(e)}")
                logger.error(f"Full error: {traceback.format_exc()}")
                raise
                
        except Exception as e:
            logger.error(f"Error in parse_document: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise 