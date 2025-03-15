import React from 'react';
import { Link } from 'react-router-dom';
import './WelcomeScreen.css';

function WelcomeScreen() {
    return (
        <div className="welcome-screen">
            <div className="welcome-content">
                <h1>Welcome to AI Image Editor</h1>
                <p>Make your photos pop with AI! Just tell us what you want, and our AI will handle the rest — from enhancing people to adjusting backgrounds to editing the whole image just by vibes, all in one easy step.</p>
                <Link to="/tutorial">
                    <button className="get-started-button">Get Started</button>
                </Link>
            </div>
        </div>
    );
}

export default WelcomeScreen;
