# Talent Lens Backend

AI-powered talent matching system that processes resumes and job descriptions to find the best matches.

## Overview

This system consists of three main components:
1. Job Description Parser (`00-parse-job-desc.py`)
2. Resume Parser (`01-parse-resume.py`)
3. Fit Score Calculator (`02-fit-score.py`)

## Prerequisites

- Python 3.9 or higher
- Poetry (package manager)
- LlamaCloud API key
- OpenAI API key

## Setup

1. Install Poetry (package manager):   ```bash
   # Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

   # Unix/macOS
   curl -sSL https://install.python-poetry.org | python3 -   ```

2. Clone the repository and install dependencies:   ```bash
   cd backend
   poetry install   ```

3. Create a `.env` file in the `backend` directory with your API keys:   ```env
   LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4-turbo-preview  # or your preferred model   ```

## Directory Structure

```
backend/
├── doc_job_desc/          # Input job description files (.pdf, .docx, .txt)
├── doc_resumes/           # Input resume files (.pdf, .docx)
├── parsed_job_desc/       # Processed job descriptions
│   ├── json/             # Structured JSON output
│   ├── markdown/         # Intermediate markdown files
│   └── original/         # Successfully processed source files
├── parsed_resumes/       # Processed resumes
│   ├── json/            # Structured JSON output
│   ├── markdown/        # Intermediate markdown files
│   └── original/        # Successfully processed source files
├── relevance_score/     # Generated fit scores
├── utils/               # Utility functions and schemas
│   ├── prompting_instructions.py  # AI system prompts
│   ├── resume_schema.py          # Pydantic models
│   └── setup_directories.py      # Directory setup utility
└── .env                 # Environment variables (not in git)
```

## Usage

1. Place job description files in `doc_job_desc/` directory
2. Place resume files in `doc_resumes/` directory
3. Run the parsers in sequence:

   ```bash
   # Parse job descriptions
   poetry run python 00-parse-job-desc.py

   # Parse resumes
   poetry run python 01-parse-resume.py

   # Generate fit scores
   poetry run python 02-fit-score.py
   ```

## File Processing Flow

1. **Job Description Parser (`00-parse-job-desc.py`)**
   - Reads PDF/DOCX/TXT files from `doc_job_desc/`
   - Converts to markdown using LlamaParse
   - Structures data using OpenAI
   - Saves JSON output in `parsed_job_desc/json/`

2. **Resume Parser (`01-parse-resume.py`)**
   - Reads PDF/DOCX files from `doc_resumes/`
   - Converts to markdown using LlamaParse
   - Structures data using OpenAI with Pydantic validation
   - Saves JSON output in `parsed_resumes/json/`

3. **Fit Score Calculator (`02-fit-score.py`)**
   - Reads processed job descriptions and resumes
   - Calculates fit scores using OpenAI
   - Saves results in `relevance_score/`

## Error Handling

- All scripts include error handling and logging
- Failed files will be reported in the console
- API key validation is performed at startup
- Original files are moved to `original/` directory after successful processing

## Development

- Code formatting: `poetry run black .`
- Linting: `poetry run flake8`
- Type checking: `poetry run mypy .`

## Dependencies

- `llama-parse`: Document parsing
- `openai`: AI processing
- `python-dotenv`: Environment management
- `pydantic`: Data validation
- `colorama`: Console output formatting

## Note

Make sure to keep your API keys secure and never commit those keys to version control. The `.env` file is included in `.gitignore` for this reason.