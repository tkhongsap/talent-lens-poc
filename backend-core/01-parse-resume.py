import os
from os import environ
from os.path import join, splitext, basename, dirname, abspath
from llama_parse import LlamaParse
from dotenv import load_dotenv
from openai import OpenAI
from utils.resume_schema import ResumeOutput  # Import the schema from utils
from utils.prompting_instructions import RESUME_PARSER_SYSTEM_PROMPT  # Import the system prompt
import json

# Get absolute paths
BACKEND_DIR = dirname(abspath(__file__))
ENV_PATH = join(BACKEND_DIR, '.env')
DOCS_DIR = join(BACKEND_DIR, 'doc_resumes')
JSON_DIR = join(BACKEND_DIR, 'parsed_resumes', 'json')
MARKDOWN_DIR = join(BACKEND_DIR, 'parsed_resumes', 'markdown')
ORIGINAL_DIR = join(BACKEND_DIR, 'parsed_resumes', 'original')  # New directory for processed files

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
        if filename.endswith(('.pdf', '.docx')):
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
                            "content": RESUME_PARSER_SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": f"Parse this resume into structured JSON:\n\n{markdown_content}"
                        }
                    ],
                    temperature=0.3,
                    seed=42
                )
                
                # Parse the response
                json_response = json.loads(completion.choices[0].message.content)
                
                # Validate with Pydantic
                resume_output = ResumeOutput.model_validate(json_response)
                
                # Save JSON output
                base_name = splitext(basename(input_path))[0]
                json_file = join(JSON_DIR, f"{base_name}.json")
                
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(resume_output.model_dump(exclude_none=True), f, indent=2)
                print(f"Saved JSON to: {json_file}")

                # After successful processing, move the original file
                original_file_path = join(ORIGINAL_DIR, filename)
                # Check if file exists and remove it before moving
                if os.path.exists(original_file_path):
                    os.remove(original_file_path)
                os.rename(input_path, original_file_path)
                print(f"Moved original file to: {original_file_path}")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                raise e  # Re-raise to see the full error stack

except Exception as e:
    print(f"Error initializing parser: {str(e)}")

print("Processing complete.")
