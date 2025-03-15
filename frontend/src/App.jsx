import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import WelcomeScreen from './components/WelcomeScreen';
import Tutorial from './components/Tutorial';
import ChatInterface from './components/ChatInterface';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<WelcomeScreen />} />
                <Route path="/tutorial" element={<Tutorial />} />
                <Route path="/chat" element={<ChatInterface />} />
            </Routes>
        </Router>
    );
}

export default App;