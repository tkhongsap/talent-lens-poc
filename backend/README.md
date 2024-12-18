# TalentLens Backend

This is the backend service for the TalentLens platform, providing APIs for resume processing, professional search, and analytics.

## Setup

1. Install Poetry (Python dependency management):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=mongodb://localhost:27017
JWT_SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LLAMA_CLOUD_API_KEY=your-llama-cloud-api-key
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-1106-preview
UPLOAD_FOLDER=uploads
```

4. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Development

- Format code:
```bash
poetry run black .
poetry run isort .
```

- Run linting:
```bash
poetry run flake8
```

- Run tests:
```bash
poetry run pytest
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── mongodb.py
│   │   └── models.py
│   ├── services/
│   │   ├── resume_processor.py
│   │   ├── search.py
│   │   └── analytics.py
│   └── main.py
├── tests/
├── .env
├── pyproject.toml
├── poetry.lock
└── README.md
```