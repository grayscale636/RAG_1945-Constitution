import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Menu from './components/Menu';
import Chatbot from './components/Chatbot';
import HomePage from './components/HomePage';
import HistoryDisplay from './components/HistoryDisplay'; // Pastikan ini diimpor

function App() {
    return (
        <Router>
            <div>
                <Menu />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/history" element={<HistoryDisplay />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;