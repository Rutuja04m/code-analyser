// App.js
import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import AnalysisResult from './components/AnalysisResult';
import './App.css';

function App() {
  const [result, setResult] = useState(null);

  const handleUpload = (data) => {
    setResult(data);
  };

  return (
    <div className="app-container">
      <UploadForm onUpload={handleUpload} />
      <AnalysisResult result={result} />
    </div>
  );
}

export default App;
