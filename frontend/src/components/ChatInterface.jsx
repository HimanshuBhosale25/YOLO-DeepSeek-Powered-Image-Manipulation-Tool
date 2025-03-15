import React, { useState, useRef } from 'react';
import axios from 'axios';
import './ChatInterface.css';

function ChatInterface() {
    const [image, setImage] = useState(null);
    const [originalImageData, setOriginalImageData] = useState(null);
    const [prompt, setPrompt] = useState('');
    const [processedImage, setProcessedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);
    const [sessionId, setSessionId] = useState(null);

    const handleImageChange = async (event) => {
        const file = event.target.files[0];
        setImage(file);
        setProcessedImage(null);
        if (file) {
            const reader = new FileReader();
            reader.onloadend = async () => {
                setOriginalImageData(reader.result);
                const formData = new FormData();
                formData.append('file', file);
                try {
                    const response = await axios.post('http://localhost:8000/create_session/', formData);
                    setSessionId(response.data.session_id);
                } catch (err) {
                    setError('Error creating session: ' + err.message);
                }
            };
            reader.readAsDataURL(file);
        } else {
            setOriginalImageData(null);
            setSessionId(null);
        }
    };

    const handlePromptChange = (event) => {
        setPrompt(event.target.value);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('session_id', sessionId);

        try {
            const endpoint = 'http://localhost:8000/process_all_adjustments/';
            const response = await axios.post(endpoint, formData, {
                responseType: 'blob',
            });
            setProcessedImage(URL.createObjectURL(response.data));
        } catch (err) {
            setError('Error processing image: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current.click();
    };

    const handleDownloadClick = () => {
        if (processedImage) {
            const a = document.createElement('a');
            a.href = processedImage;
            a.download = 'modified_image.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    };

    return (
        <div className={`chat-interface ${originalImageData ? 'image-uploaded' : ''}`}>
            <div className="input-title-wrapper">
                <h1 className="app-title">Image Editor</h1>
                <div className="upload-container">
                    <button onClick={handleUploadClick} className="upload-button">
                        {image ? image.name : 'Upload Image'}
                    </button>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleImageChange}
                        className="input-file"
                        style={{ display: 'none' }}
                        accept="image/*"
                    />
                </div>
            </div>

            <div className="input-area">
                <textarea
                    id="promptInput"
                    placeholder="Enter prompt (e.g., vintage, warm, artistic)"
                    value={prompt}
                    onChange={handlePromptChange}
                    className="prompt-textarea"
                />
                <button onClick={handleSubmit} disabled={loading} className={`process-button ${loading ? 'loading' : ''}`}>
                    {loading ? 'Processing...' : 'Process Image'}
                </button>
            </div>

            {error && <p className="error-message">{error}</p>}

            <div className="image-content-wrapper">
                {(originalImageData || processedImage) && (
                    <div className="image-display-container">
                        {originalImageData && (
                            <div className="image-display">
                                <p className="image-label">Original Image</p>
                                <img src={originalImageData} alt="Original" className="processed-image" />
                            </div>
                        )}
                        {processedImage && (
                            <div className="image-display">
                                <p className="image-label">Edited Image</p>
                                <img src={processedImage} alt="Processed" className="processed-image" />
                            </div>
                        )}
                    </div>
                )}
                {processedImage && (
                    <div className="download-button-container">
                        <button onClick={handleDownloadClick} className="download-button">
                            Download Image
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ChatInterface;