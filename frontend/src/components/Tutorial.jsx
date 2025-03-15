import React from 'react';
import { Link } from 'react-router-dom';
import './Tutorial.css';

function Tutorial() {
    return (
        <div className="tutorial-screen">
            <div className="tutorial-content">
                <h2>How to Use AI Image Editor</h2>
                <ol>
                    <li>Upload your image.</li>
                    <li>Select what to edit: "Object", "Background", or "Full Image".</li>
                    <li>Describe your edit, e.g., "Make me look vibrant" or "Turn the background black and white".</li>
                    <li>For pro edits, request color tone or lighting adjustments.</li>
                    <li>Click "Process Image" to apply changes.</li>
                    <li>Stack multiple edits by adding more prompts.</li>
                    <li>Try creative prompts for unique "vibe-based" transformations.</li>
                    <li>Download your final image!</li>
                </ol>
                <Link to="/chat">
                    <button className="go-to-chat-button">Go to Editor</button>
                </Link>
            </div>
        </div>
    );
}

export default Tutorial;
