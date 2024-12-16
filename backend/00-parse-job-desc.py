import os
from os import environ
from os.path import join, splitext, basename, dirname, abspath
from llama_parse import LlamaParse
from dotenv import load_dotenv
from openai import OpenAI
from utils.resume_schema import ResumeOutput  # Import the schema from utils
import json

# Get absolute paths
BACKEND_DIR = dirname(abspath(__file__))
ENV_PATH = join(BACKEND_DIR, '.env')
DOCS_DIR = join(BACKEND_DIR, 'doc_job_desc')  # Change to job descriptions directory
JSON_DIR = join(BACKEND_DIR, 'parsed_job_desc', 'json')  # Change to job descriptions output directory
MARKDOWN_DIR = join(BACKEND_DIR, 'parsed_job_desc', 'markdown')  # Change to job descriptions output directory
ORIGINAL_DIR = join(BACKEND_DIR, 'parsed_job_desc', 'original')  # Change to job descriptions output directory

# Debug: Print the actual path we're trying to load
print(f"Loading .env from: {ENV_PATH}")

# Load environment variables from backend/.env
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH, override=True)  # Added override=True to ensure our values take precedence

# Get and verify environment variables
llama_cloud_api_key = environ.get("LLAMA_CLOUD_API_KEY")
openai_api_key = environ.get("OPENAI_API_KEY")
llm_model = environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Debug: Print the first few characters of the actual values
print(f"LLAMA_CLOUD_API_KEY: {llama_cloud_api_key[:20] if llama_cloud_api_key else 'Not found'}...")
print(f"OPENAI_API_KEY: {openai_api_key[:20] if openai_api_key else 'Not found'}...")

# Verify we have the actual values, not placeholders
if "your_" in str(llama_cloud_api_key) or "your_" in str(openai_api_key):
    raise ValueError("Found placeholder values in API keys. Please update .env with actual API keys")

# Validate API keys
if not llama_cloud_api_key:
    raise ValueError("LLAMA_CLOUD_API_KEY not found in environment variables")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

try:
    # Initialize parsers
    llama_parser = LlamaParse(
        api_key=llama_cloud_api_key,
        result_type="markdown"
    )
    
    openai_client = OpenAI(api_key=openai_api_key)

    # Create output directory if it doesn't exist
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    if not os.path.exists(MARKDOWN_DIR):
        os.makedirs(MARKDOWN_DIR)
    if not os.path.exists(ORIGINAL_DIR):
        os.makedirs(ORIGINAL_DIR)

    # Process all files in docs directory
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(('.pdf', '.docx', '.txt')):
            input_path = join(DOCS_DIR, filename)
            try:
                print(f"Processing: {filename}")
                
                # Step 1: Parse document to markdown
                documents = llama_parser.load_data(input_path)
                markdown_content = "\n\n".join([doc.text for doc in documents])
                
                # Save markdown content
                base_name = splitext(basename(input_path))[0]
                markdown_file = join(MARKDOWN_DIR, f"{base_name}.md")
                with open(markdown_file, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                print(f"Saved markdown to: {markdown_file}")
                
                # Step 2: Use OpenAI to convert markdown to structured JSON
                completion = openai_client.chat.completions.create(
                    model=llm_model,
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a precise job description parser. Convert the job description into a structured JSON format that matches this schema:
                            {
                                "job_title": "Title of the job",
                                "company": "Company offering the job",
                                "location": "Location of the job",
                                "employment_type": "Full-time, Part-time, Contract, etc.",
                                "responsibilities": ["List of job responsibilities"],
                                "qualifications": ["List of required qualifications"],
                                "skills": ["List of required skills"],
                                "benefits": ["List of benefits offered"],
                                "application_process": "Description of the application process"
                            }

                            Rules:
                            1. Extract actual information from the job description - do not include placeholder text
                            2. For missing information, use null instead of placeholder text
                            3. Ensure all URLs start with https://
                            4. Do not include explanatory text like 'string or null' in the output"""
                        },
                        {
                            "role": "user",
                            "content": f"Parse this job description into structured JSON:\n\n{markdown_content}"
                        }
                    ],
                    temperature=0.1,
                    seed=42
                )
                
                # Parse the response
                json_response = json.loads(completion.choices[0].message.content)
                
                # Save JSON output
                base_name = splitext(basename(input_path))[0]
                json_file = join(JSON_DIR, f"{base_name}.json")
                
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(json_response, f, indent=2)
                print(f"Saved JSON to: {json_file}")

                # After successful processing, move the original file
                original_file_path = join(ORIGINAL_DIR, filename)
                os.rename(input_path, original_file_path)
                print(f"Moved original file to: {original_file_path}")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                raise e  # Re-raise to see the full error stack

except Exception as e:
    print(f"Error initializing parser: {str(e)}")

print("Processing complete.")
