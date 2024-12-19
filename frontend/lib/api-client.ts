const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const uploadResumes = async (files: File[]): Promise<{ file_id: string }> => {
  if (!files || files.length === 0) {
    throw new Error('No files provided');
  }
  
  const formData = new FormData();
  formData.append('file', files[0]);
  
  const response = await fetch(`${API_BASE_URL}/uploads/resume`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Upload failed: ${errorText}`);
  }
  
  return response.json();
};

export async function uploadJobDescription(file: File) {
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
}

export async function uploadJobDescriptionText(text: string) {
  const response = await fetch(`${API_BASE_URL}/uploads/job-description-text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(error.detail || 'Job description text upload failed');
  }

  return response.json();
}

export async function analyzeResume(resumeId: string, jobDescriptionId: string) {
  const response = await fetch(`${API_BASE_URL}/analysis`, {
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
    const error = await response.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(error.detail || 'Resume analysis failed');
  }

  return response.json();
} 