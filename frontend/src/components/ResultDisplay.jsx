import React from 'react';

function ResultDisplay({ response }) {
    return (
        <div className="result">
            <h2>Hasil Jawaban</h2>
            <p>{response}</p>
        </div>
    );
}

export default ResultDisplay;