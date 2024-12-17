import os
from os.path import join, dirname, abspath

BACKEND_DIR = dirname(dirname(abspath(__file__)))  # Get backend directory

# Define all required directories
DIRECTORIES = [
    'doc_job_desc',
    'doc_resumes',
    'parsed_job_desc/json',
    'parsed_job_desc/markdown',
    'parsed_job_desc/original',
    'parsed_resumes/json',
    'parsed_resumes/markdown',
    'parsed_resumes/original',
    'relevance_score'
]

def setup_directories():
    """Create all required directories and their .gitkeep files"""
    for dir_path in DIRECTORIES:
        # Create full path
        full_path = join(BACKEND_DIR, dir_path)
        
        # Create directory if it doesn't exist
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")
        
        # Create .gitkeep file
        gitkeep_path = join(full_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                pass  # Create empty file
            print(f"Created .gitkeep in: {full_path}")

if __name__ == "__main__":
    setup_directories()