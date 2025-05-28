import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import './AnalysisResult.css';

const AnalysisResult = ({ result }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (result && result.flowchart && chartRef.current) {
      mermaid.initialize({ startOnLoad: false });
      try {
        mermaid.render('flowchartDiagram', result.flowchart, (svgCode) => {
          chartRef.current.innerHTML = svgCode;
        });
      } catch (err) {
        chartRef.current.innerHTML = "<p>Failed to render flowchart.</p>";
      }
    }
  }, [result]);

  if (!result) return null;

  return (
    <div className="result-container">
      <div className="result-box">
        <h2>{result.filename}</h2>

        {/*  Function Analysis */}
        {result.analysis.functions.map((fn, j) => (
          <div key={j} className="function-block">
            <h3>{fn.name}</h3>
            <p><strong>Args:</strong> {fn.args.join(', ')}</p>
            <pre>{fn.analysis}</pre>
          </div>
        ))}

        {/*  Flowchart below analysis */}
        {result.flowchart && (
          <div className="function-block">
            <h3>Code Flowchart</h3>
            <div ref={chartRef} className="flowchart-box" />
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisResult;
