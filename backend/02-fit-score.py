import os
import json
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from openai import OpenAI
from utils.prompting_instructions import FIT_SCORE_SYSTEM_PROMPT  # Import the prompt
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

# Define directories
BACKEND_DIR = dirname(abspath(__file__))
ENV_PATH = join(BACKEND_DIR, '.env')
JOB_DESC_DIR = join(BACKEND_DIR, 'parsed_job_desc', 'json')
RESUME_DIR = join(BACKEND_DIR, 'parsed_resumes', 'json')
OUTPUT_DIR = join(BACKEND_DIR, 'relevance_score')

# Debug: Print the actual path we're trying to load
print(f"{Fore.CYAN}Loading .env from: {Style.BRIGHT}{ENV_PATH}{Style.RESET_ALL}")

# Load environment variables from backend/.env
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH, override=True)  # Added override=True to ensure our values take precedence

# Get and verify environment variables
llama_cloud_api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
llm_model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load job description
job_desc_file = join(JOB_DESC_DIR, 'JD-Data-Engineer.json')  # Example file
with open(job_desc_file, 'r', encoding='utf-8') as f:
    job_desc = json.load(f)

# Function to calculate fit score using OpenAI
def calculate_fit_score_with_llm(resume, job_desc):
    # Use the imported system prompt
    system_prompt = FIT_SCORE_SYSTEM_PROMPT

    # Prepare the input for the model
    input_content = {
        "job_description": job_desc,
        "resume": resume
    }

    try:
        # Call OpenAI API
        completion = openai_client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(input_content)}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        # Get the response content
        response_content = completion.choices[0].message.content
        print(f"{Fore.MAGENTA}Raw API Response: {Style.BRIGHT}{response_content}{Style.RESET_ALL}")  # Debug print

        try:
            # Parse the response
            fit_score = json.loads(response_content)
            return fit_score
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {response_content}")
            raise

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise

# Process all resumes in the directory
resume_files = [f for f in os.listdir(RESUME_DIR) if f.endswith('.json')]
print(f"\n{Fore.CYAN}{Style.BRIGHT}Found {len(resume_files)} resume files to process{Style.RESET_ALL}")

for resume_filename in resume_files:
    print(f"\n{Fore.BLUE}{Style.BRIGHT}Processing resume: {resume_filename}{Style.RESET_ALL}")
    
    # Load resume
    resume_file = join(RESUME_DIR, resume_filename)
    try:
        with open(resume_file, 'r', encoding='utf-8') as f:
            resume = json.load(f)

        # Calculate fit score using OpenAI
        fit_score = calculate_fit_score_with_llm(resume, job_desc)

        # Save output
        output_file = join(OUTPUT_DIR, f"fit_score_{resume_filename}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fit_score, f, indent=2)
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Saved fit score to: {output_file}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error processing {resume_filename}: {e}{Style.RESET_ALL}")
        continue  # Continue with next resume even if one fails