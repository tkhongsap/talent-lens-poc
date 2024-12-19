const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const uploadJobDescription = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/uploads/job-description`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(error.detail || 'Job description upload failed');
  }
  
  return response.json();
};

export const uploadResumes = async (files: File[]) => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('file', file);
  });
  
  const response = await fetch(`${API_BASE_URL}/uploads/resume`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Failed to upload resume');
  }
  
  return response.json();
};

export const uploadJobDescriptionText = async (text: string) => {
  const response = await fetch(`${API_BASE_URL}/uploads/job-description-text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to upload job description text');
  }
  
  return response.json();
};

export const analyzeResume = async (resumeId: string, jobDescriptionId: string) => {
  const response = await fetch(`${API_BASE_URL}/analysis/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      resume_id: resumeId,
      job_description_id: jobDescriptionId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to analyze resume');
  }

  return response.json();
}; 