import React, { useState } from 'react';

function InputForm({ onResponse }) {
    const [question, setQuestion] = useState(''); // State untuk menyimpan pertanyaan

    const handleSubmit = async (e) => {
        e.preventDefault(); // Mencegah reload halaman

        // Panggil onResponse untuk menambahkan pesan pengguna ke tampilan
        onResponse({ question, answer: '' }); // Tambahkan pesan pengguna tanpa jawaban

        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }), // Mengirim pertanyaan ke backend
        });

        if (response.ok) {
            const data = await response.json();
            onResponse({ question, answer: data.answer }); // Mengirim kembali pertanyaan dan jawaban ke komponen Chatbot
            setQuestion(''); // Mengosongkan input setelah pengiriman
        } else {
            console.error('Error:', response.statusText);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)} // Mengupdate state saat input berubah
                placeholder="Masukkan pertanyaan hukum"
                className="form-control"
            />
            <button className="btn btn-primary" type="submit">Tanya</button>
        </form>
    );
}

export default InputForm;