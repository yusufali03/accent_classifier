// src/api.js
const API = import.meta.env.VITE_API;

// Link-based analysis
export async function analyzeVideo(url) {
  const response = await fetch(`${API}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Request failed');
  }

  return await response.json();
}

// File upload-based analysis
export async function analyzeFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API}/api/analyze-upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'File upload failed');
  }

  return await response.json();
}
