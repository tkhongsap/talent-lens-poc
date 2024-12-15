# Resume Parser Backend Service

An intelligent resume parsing service that converts PDF and DOCX resumes into structured JSON data. Built with Python, it leverages LlamaParse for document conversion and OpenAI's GPT models for accurate information extraction, making resume data easily processable for ATS (Applicant Tracking Systems) and HR applications.

## Features

- Converts PDF and DOCX resumes to markdown format using LlamaParse
- Transforms markdown content into structured JSON using OpenAI
- Validates output using Pydantic models
- Supports multiple resume sections including:
  - Contact Information
  - Work Experience
  - Education
  - Skills
  - Additional Information

## Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- LlamaParse API key
- OpenAI API key

## Installation

1. Clone the repository: 