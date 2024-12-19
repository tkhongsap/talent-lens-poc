# TalentLens Backend

This is the backend service for the TalentLens platform, providing APIs for resume processing, professional search, and analytics.

## Features

- Resume parsing and analysis
- Job description parsing
- AI-powered matching between resumes and job descriptions
- Professional search capabilities
- Analytics and insights

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── analysis.py
│   │           └── uploads.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── mongodb.py
│   │   └── models.py
│   ├── scripts/
│   │   ├── 00-parse-job-desc.py
│   │   ├── 01-parse-resume.py
│   │   └── 02-fit-score.py
│   ├── services/
│   │   ├── analytics.py
│   │   ├── llama_parser.py
│   │   ├── openai_service.py
│   │   ├── parser_service.py
│   │   ├── resume_processor.py
│   │   └── search.py
│   └── utils/
│       ├── prompting_instructions.py
│       └── resume_schema.py
├── tests/
├── .env.example
├── .gitignore
└── pyproject.toml
```

## Setup

1. Install Poetry (Python dependency management):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:
```env
# Database settings
DATABASE_URL=mongodb://localhost:27017

# Authentication settings
JWT_SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
LLAMA_CLOUD_API_KEY=your-llama-cloud-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Upload settings
UPLOAD_FOLDER=uploads
```

5. Create required directories:
```bash
mkdir -p uploads processed/resumes
```

6. Download spaCy model:
```bash
poetry run python -m spacy download en_core_web_sm
```

7. Run the development server:
```bash
poetry run uvicorn app.main:app --reload

or

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

## API Endpoints

The API will be available at:
- API Root: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Status: http://localhost:8000/health

Available endpoints:
- `GET /`: Welcome page
- `GET /health`: System health status
- `POST /api/v1/analyze/analyze`: Analyze resume against job description
- `POST /api/v1/uploads/resume`: Upload resumes
- `POST /api/v1/uploads/job-description`: Upload job description file
- `POST /api/v1/uploads/job-description/text`: Upload job description as text

## Development Commands

Format code:
```bash
# Run Black formatter
poetry run black .

# Sort imports
poetry run isort .
```

Run linting:
```bash
poetry run flake8
```

Run tests:
```bash
poetry run pytest
```

## Utility Scripts

The `app/scripts` directory contains utility scripts for processing documents:

### Resume Parser
Process resume documents:
```bash
poetry run python -m app.scripts.01-parse-resume
```

### Job Description Parser
Parse job description documents:
```bash
poetry run python -m app.scripts.00-parse-job-desc
```

### Fit Score Calculator
Calculate match scores between resumes and job descriptions:
```bash
poetry run python -m app.scripts.02-fit-score
```

## Directory Structure

- `uploads/`: Stores uploaded files
- `processed/resumes/`: Stores processed resume files
- `processed/job-desc/`: Stores processed job description files
- `app/scripts/`: Contains utility scripts for document processing
- `app/services/`: Core services for parsing and analysis
- `app/api/`: API endpoints and routes
- `app/utils/`: Shared utilities and schemas

## License

Proprietary. All rights reserved.