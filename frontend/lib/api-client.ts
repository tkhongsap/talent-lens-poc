const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function uploadResumes(files: File[]) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await fetch('/api/v1/uploads/resume', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to upload resumes');
  }

  return response.json();
}

export async function uploadJobDescription(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/v1/uploads/job-description', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to upload job description');
  }

  return response.json();
} 