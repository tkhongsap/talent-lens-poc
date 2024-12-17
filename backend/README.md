# TalentLens Backend

This is the backend service for the TalentLens platform, providing APIs for resume processing, professional search, and analytics.

## Features

- User Management & Authentication
- Resume Processing & Analysis
- Professional Search
- Analytics & Matching
- Secure File Storage
- API Documentation

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=mongodb://localhost:27017
JWT_SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── routes.py
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
├── requirements.txt
└── README.md
```

## Testing

Run tests using pytest:
```bash
pytest
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 