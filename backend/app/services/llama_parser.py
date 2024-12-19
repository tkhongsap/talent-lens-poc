from llama_parse import LlamaParse
from typing import List
import os
import logging
import traceback

logger = logging.getLogger(__name__)

class LlamaParser:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Llama Cloud API key is required")
        
        self.parser = LlamaParse(
            api_key=api_key,
            result_type="markdown",
            verbose=True,
            num_workers=1
        )
    
    def parse_document(self, file_path: str) -> str:
        """
        Parse a document file into markdown format
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            str: Markdown content of the document
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            # Parse document using LlamaParse
            logger.info(f"Starting parse for: {file_path}")
            documents = self.parser.load_data(file_path)
            
            if not documents:
                logger.error("No content extracted")
                raise ValueError("Document parsing returned empty result")
                
            logger.info(f"Successfully extracted {len(documents)} sections")
            
            # Combine all document sections into one markdown string
            markdown_content = "\n\n".join([doc.text for doc in documents])
            logger.info(f"Generated markdown content length: {len(markdown_content)}")
            
            return markdown_content
            
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            logger.error(f"Full error: {traceback.format_exc()}")
            raise