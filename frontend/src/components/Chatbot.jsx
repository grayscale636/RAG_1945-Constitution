import React, { useState, useRef, useEffect } from 'react';
import InputForm from './InputForm';

function Chatbot() {
    const [messages, setMessages] = useState([]);
    const chatEndRef = useRef(null); // Referensi untuk elemen akhir chat

    const loadMessages = () => {
        const savedMessages = localStorage.getItem('chatMessages');
        if (savedMessages) {
            setMessages(JSON.parse(savedMessages));
        }
    };

    const saveMessages = (newMessages) => {
        localStorage.setItem('chatMessages', JSON.stringify(newMessages));
    };

    const handleResponse = (data) => {
        // Tambahkan pesan pengguna ke dalam state
        const newMessages = [...messages, { text: data.question, type: 'user' }];
        setMessages(newMessages);
        saveMessages(newMessages);
        
        // Jika ada jawaban, tambahkan ke dalam state
        if (data.answer) {
            const aiMessage = { text: data.answer, type: 'ai' };
            setMessages((prevMessages) => [...prevMessages, aiMessage]);
            saveMessages([...newMessages, aiMessage]);
        }
    };

    const scrollToBottom = () => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        loadMessages();
    }, []);

    const clearMessages = () => {
        if (window.confirm("Apakah Anda yakin ingin menghapus semua pesan?")) {
            setMessages([]);
            localStorage.removeItem('chatMessages'); // Hapus dari localStorage
        }
    };

    return (
        <div className="container mt-4 chatbot-container">
            <h2 className="text-primary">Law</h2>
            <div className="chat-container w-100">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.type === 'user' ? 'user-message' : 'ai-message'}`}
                    >
                        {msg.text}
                    </div>
                ))}
                <div ref={chatEndRef} /> {/* Elemen untuk menggulir ke bawah */}
            </div>
            <InputForm onResponse={handleResponse} />
            <button 
                className="btn btn-danger btn-small mt-3" // Menggunakan kelas CSS yang sama
                onClick={clearMessages} 
            >
                Delete History
            </button>
        </div>
    );
}

export default Chatbot;