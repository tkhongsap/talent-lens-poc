const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function uploadResumes(files: File[]) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await fetch(`${API_BASE_URL}/uploads/resume`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to upload resumes' }));
    throw new Error(error.detail || 'Failed to upload resumes');
  }

  return response.json();
}

export async function uploadJobDescription(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/uploads/job-description`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to upload job description' }));
    throw new Error(error.detail || 'Failed to upload job description');
  }

  return response.json();
}

export async function uploadJobDescriptionText(text: string) {
  const response = await fetch(`${API_BASE_URL}/uploads/job-description/text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to upload job description text' }));
    throw new Error(error.detail || 'Failed to upload job description text');
  }

  return response.json();
} 