from llama_parse import LlamaParse
from typing import List
import os

class LlamaParser:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Llama Cloud API key is required")
        
        self.parser = LlamaParse(
            api_key=api_key,
            result_type="markdown"
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
            documents = self.parser.load_data(file_path)
            
            # Combine all document sections into one markdown string
            markdown_content = "\n\n".join([doc.text for doc in documents])
            
            return markdown_content
            
        except Exception as e:
            raise Exception(f"Error parsing document: {str(e)}")