import React, { useEffect, useState } from 'react';

function HistoryDisplay() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        const response = await fetch('http://localhost:8000/history');
        const data = await response.json();
        setHistory(data);
    };

    // Fungsi untuk menghapus riwayat chat
    const clearHistory = async () => {
        if (window.confirm("Apakah Anda yakin ingin menghapus semua riwayat chat?")) {
            const response = await fetch('http://localhost:8000/clear_history', { method: 'DELETE' });
            if (response.ok) {
                setHistory([]); // Kosongkan state
            } else {
                console.error('Gagal menghapus riwayat chat');
            }
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="text-primary">Riwayat Chat</h2>
            <ul className="list-group">
                {history.map((item) => (
                    <li key={item.id} className="list-group-item">
                        <strong>Pertanyaan:</strong> {item.question}<br />
                        <strong>Jawaban:</strong> {item.answer}
                    </li>
                ))}
            </ul>
            <button 
                className="btn btn-danger btn-small" // Menggunakan kelas CSS baru
                onClick={clearHistory} 
            >
                Delete History
            </button>
        </div>
    );
}

export default HistoryDisplay;