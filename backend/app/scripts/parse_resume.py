import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from llama_parse import LlamaParse
from ..utils.prompting_instructions import RESUME_PARSER_SYSTEM_PROMPT
from ..utils.resume_schema import ResumeOutput
from typing import List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize API clients
        self.llama_parser = LlamaParse(api_key=os.getenv("LLAMA_CLOUD_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
        
        # Set up directories
        self.input_dir = Path("uploads/resumes")
        self.output_dir = Path("processed/resumes")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def parse_single_resume(self, file_path: Path) -> ResumeOutput:
        """Parse a single resume file and return structured data"""
        try:
            logger.info(f"Processing resume: {file_path}")
            
            # First pass: Convert to markdown using LlamaParse
            markdown_content = self.llama_parser.parse_document(
                file_path,
                result_type="markdown"
            )
            
            # Second pass: Structure the content using OpenAI
            completion = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": RESUME_PARSER_SYSTEM_PROMPT},
                    {"role": "user", "content": markdown_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            # Parse and validate the response
            json_response = json.loads(completion.choices[0].message.content)
            resume_output = ResumeOutput.model_validate(json_response)
            
            # Save the processed output
            output_file = self.output_dir / f"{file_path.stem}_processed.json"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(resume_output.model_dump_json(indent=2))
            
            logger.info(f"Successfully processed resume: {file_path}")
            return resume_output
            
        except Exception as e:
            logger.error(f"Error processing resume {file_path}: {str(e)}")
            raise

    async def process_directory(self) -> List[ResumeOutput]:
        """Process all resume files in the input directory"""
        results = []
        
        # Supported file extensions
        supported_extensions = {".pdf", ".docx", ".doc", ".txt"}
        
        try:
            for file_path in self.input_dir.iterdir():
                if file_path.suffix.lower() in supported_extensions:
                    try:
                        result = await self.parse_single_resume(file_path)
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Failed to process {file_path}: {str(e)}")
                        continue
                else:
                    logger.warning(f"Skipping unsupported file: {file_path}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing directory: {str(e)}")
            raise

async def main():
    """Main entry point for the resume parsing script"""
    try:
        parser = ResumeParser()
        results = await parser.process_directory()
        logger.info(f"Successfully processed {len(results)} resumes")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# ... rest of the script ... 