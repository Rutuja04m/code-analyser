//UploadForm.js

import React, { useState } from 'react';
import './UploadForm.css';

const UploadForm = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload-analyze/`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      onUpload(data);
    } catch (err) {
      setError('Upload or analysis failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-box">
      <h1>AI Code Analyzer</h1>
      <input type="file" accept=".py" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={uploading || !file}>
        {uploading ? 'Analyzing...' : 'Analyze'}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default UploadForm;
