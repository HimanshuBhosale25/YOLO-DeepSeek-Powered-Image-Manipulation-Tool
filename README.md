# AI Image Transformer: Deep Learning Powered Image Editing with a User-Friendly Web Interface 🧠✨🌐

**This project demonstrates the power of deepseek-r1-distill-llama-70b model to handle and manipulate complex prompts while utilizing YOLOv8l-seg model for segmentation and Pillow library for image manipulation, packaged within a user-friendly web application. It highlights the synergy between advanced AI models and modern frontend development, making complex image editing accessible to professional editors as well as general audience. 🚀**

## Key Deep Learning and AI Features 🌟

* **AI-Driven Image Manipulation:** Witness the transformative power of large language models as your text prompts are translated into precise and nuanced image edits. 🧠
* **Advanced Object Segmentation (YOLOv8):** Leveraging Ultralytics' YOLOv8l-seg for accurate object detection and segmentation, enabling precise, targeted edits on specific image regions. 🎯
* **Natural Language Understanding (Groq API):** Integrating with the Groq API to harness deepseek-r1-distill-llama-70b for understanding and interpreting user prompts, translating them into actionable image adjustments. 💬
* **Sophisticated Masking and Blending with OpenCV:** Implementing advanced masking, Inverted Masking and blending techniques using OpenCV, ensuring seamless integration of AI-driven edits for realistic results. 🎭
* **End-to-End Deep Learning Pipeline:** Demonstrating a complete deep learning pipeline, from natural language input to image output, showcasing the project's AI capabilities. 🔄

## User-Friendly Web Interface (React) 🌐

* **Intuitive React Frontend:** Provides a seamless and engaging user experience, showcasing modern web development practices with a clean, glassmorphic design and smooth transitions. 👀
* **Session-Based Editing with Persistent State:** Allows users to stack multiple edits, demonstrating the model's ability to maintain context and refine results across sessions, all managed within the frontend. 🔄
* **Real-time Previews:** Displays original and processed images side-by-side, providing instant feedback on the AI's performance within the browser. 🖼️
* **Download Functionality:** Enables users to easily download edited images, completing the end-to-end user experience, handled efficiently by the frontend. 📥
* **Responsive Design:** Ensures a consistent and enjoyable experience across various devices, showcasing frontend adaptability. 📱💻

## Screenshots of UI:📸

### **Welcome Screen:**
![WS](images/i4.png) 


### **Tutorial:**
![T](images/i5.png)


### **Example 1:**
![Ex1](images/i6.png)


### **Example 2:**
![Ex2](images/i7.png)


### **Example 3:**
![Ex3](images/i8.png)


## Segmentation and Masking:📸

### **Original Image:**
![OG](images/i1.png)


### **Object Detection:**
![OD](images/i2.png)


### **Object Making:**
![OM](images/i3.png)




## Getting Started (Focus on AI and Web Integration) 🏁

### Prerequisites 📋

* Node.js and npm (or yarn) installed for frontend development. 📦
* Python 3.11 with required deep learning and AI libraries (see Dependencies). 🐍
* A running backend server (see Backend Setup). ⚙️

### Installation 🛠️

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/HimanshuBhosale25/YOLO-DeepSeek-Powered-Image-Manipulation-Tool.git
    cd ai-image-editor
    ```

2.  **Install frontend dependencies:**

    ```bash
    npm install
    ```

3.  **Run the frontend:**

    ```bash
    npm start
    ```

    Open your browser and navigate to `http://localhost:5173`. 🌐

4.  **Backend Setup:**

    * Navigate to the backend directory. 📂
    * Install backend dependencies (refer to backend documentation for specific instructions. Focus on the AI and deep learning libraries). ⬇️
    * Set the `GROQ_API_KEY` environment variable. 🔑
    * Run the FastAPI application (e.g., `uvicorn main:app --reload`). ▶️
    * Ensure the backend is accessible at `http://localhost:8000`. 🚀

### Usage (AI and Web Interaction) 💡

1.  **Upload an image:** (Using the web interface to provide input for the Large Language model). 🖼️
2.  **Enter a descriptive text prompt:** (To guide the AI's image editing process through the web interface). 📝
3.  **Process the image:** (Using the web interface to trigger the deep learning pipeline). ✅
4.  **View the results:** (Using the web interface to observe the AI's output). 👀
5.  **Download:** (Using the web interface to save the AI-processed image). 💾

## Technologies Used:📦

* **Backend (Python):**
    * FastAPI ⚡
    * Uvicorn 🦄
    * Pillow (PIL) 🖼️
    * OpenCV (cv2) 👁️
    * Ultralytics (YOLOv8) 🎯
    * Groq 🤖

* **Frontend (React):**
    * React ⚛️
    * React Router DOM 🛣️
    * Axios 📡


## Contributing (AI and Web Focus) 🤝

Contributions focused on improving the deep learning models, AI integration, image processing algorithms, and the user-friendly web interface are highly encouraged. 🐛✨📈

## License 📜

This project is licensed under the MIT License. 📝