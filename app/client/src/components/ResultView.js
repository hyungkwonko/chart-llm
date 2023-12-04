// ResultView.js
import React from 'react';
import { useSelector } from 'react-redux';
import { Card } from 'react-bootstrap';

function ResultView() {
  const nl = useSelector((state) => state.text.nl);
  const isLoading = useSelector((state) => state.text.isLoading);
  const nlString = isLoading
    ? "\nGenerating NL Datasets is in progress..... Please wait!"
    : Object.entries(nl).map(([key, value]) => `Chart ${key}: ${value}`).join('\n');

  return (
    <>
      <Card className="mt-3" style={{ border: "none", backgroundColor: 'transparent' }}>
        <Card.Body style={{ border: "1px solid #C0C0C0", borderRadius: "0" }}>
          <p className='center' style={{ fontWeight: 'bold' }}>Generated NL Dataset</p>
          <textarea
            style={{ width: '100%', height: '350px', border: 'none', outline: 'none', resize: 'none', backgroundColor: 'transparent' }}
            readOnly
            value={nlString}
          ></textarea>
        </Card.Body>
      </Card>
    </>
  );
}

export default ResultView;


