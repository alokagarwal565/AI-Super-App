# AI Super App 🚀

**AI Super App** is an innovative, all-in-one web application that consolidates various powerful generative AI functionalities into a single, user-friendly platform. It empowers users with creative automation tools, including personalized image generation, AI video creation, a robust gallery management system, and an advanced AI-powered portfolio website generator.

This project aims to bridge the gap between cutting-edge AI capabilities and everyday usability, making generative AI accessible to a wide range of users, from casual enthusiasts to aspiring entrepreneurs.

## ✨ Features

* **Personalized AI Image Generation**: Generate stunning images from custom prompts, with the option to incorporate personalized facial references using fine-tuned models.
* **AI Video Generation**: Create dynamic videos from textual prompts using advanced AI models, enabling smooth transitions and high rendering fidelity.
* **AI-Powered Portfolio Website Generator**: Upload your resume (PDF or TXT) and instantly generate a professional, responsive personal portfolio website. The AI parses your content, rephrases it, and organizes it into aesthetically pleasing sections.
* **Integrated Gallery Management**: Securely store and manage all your generated images, videos, and portfolio website files within your personal gallery.
* **User Account Management**: Full-fledged user authentication system with secure sign-up, login, credit-based usage, and customizable storage.
* **Modern & Responsive UI**: A sleek, intuitive, and responsive user interface built with the latest frontend frameworks for a seamless user experience across all devices.

## 💡 Technologies Used

The AI Super App leverages a powerful stack of modern technologies to deliver its diverse functionalities:

### Frontend
* **HTML, CSS, JavaScript**: Core web technologies for structuring, styling, and interactivity.
* **React.js**: For building dynamic and reactive user interface components.
* **Tailwind CSS**: A utility-first CSS framework for rapid and responsive UI development.

### Backend
* **Flask**: A lightweight Python web framework for handling API routes, authentication, and business logic.
* **SQLAlchemy**: An Object Relational Mapper (ORM) for efficient and secure database interactions.
* **Bcrypt**: For secure password hashing and user authentication.
* **pdf-parse / PyMuPDF**: Libraries for extracting and parsing content from uploaded PDF and TXT resume files.

### AI Model Integration
* **Replicate API**: Integrates with cutting-edge models for image and video generation (e.g., Flux LoRa for face conditioning, Deforum for video generation).
* **HuggingFace APIs**: Used for custom-trained face generation models (LoRA).
* **Gemini API / Other LLMs (e.g., GPT-4)**: Powers natural language processing tasks, including parsing, rephrasing, and enhancing resume data for portfolio generation.

### Database
* **SQLite (Development)**: Lightweight database for local development.
* **PostgreSQL (Production)**: Robust relational database for scalable production environments, storing user data, credentials, and usage logs.

## 🏗️ Architecture

The AI Super App follows a modular and layered architecture designed for scalability, maintainability, and future expansion.


### Key Components:

1.  **User Interface Layer**: Built with **React/Next.js** and **Tailwind CSS**, providing intuitive interfaces for user authentication, content generation prompts, resume uploads, and viewing generated outputs.
2.  **Application Logic Layer (Flask Backend)**: Handles API requests, user authentication, credit management, and orchestrates calls to external AI services.
3.  **AI Model Interaction**: Manages communication with **Replicate**, **HuggingFace**, and **Gemini APIs**, sending input data (prompts, face images, parsed resumes) and receiving generated outputs.
4.  **Storage and Database Layer**: Utilizes **SQLAlchemy** for data modeling and queries, **bcrypt** for secure password hashing, and stores generated content (image links, website templates) in user galleries.
5.  **Output/Rendering Layer**: Renders generated media (images/videos) and HTML-based websites in real-time on the frontend, with options for download or temporary hosting.

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.8+
* Node.js & npm (or yarn)
* Git
* API keys for Replicate, HuggingFace, and Gemini (or other LLMs)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/alokagarwal565/AI-Super-App.git
    cd ai-super-app
    ```

2.  **Backend Setup:**
    ```bash
    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r backend/requirements.txt
    ```
    *Create a `.env` file in the `backend` directory and add your API keys and database configuration:*
    ```
    REPLICATE_API_TOKEN="your_replicate_api_key"
    HUGGINGFACE_API_TOKEN="your_huggingface_api_key"
    GEMINI_API_TOKEN="your_gemini_api_key"
    DATABASE_URL="sqlite:///site.db" # Or your PostgreSQL connection string
    SECRET_KEY="your_secret_flask_key"
    ```

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install # Or `yarn install`
    ```
    *Create a `.env` file in the `frontend` directory and add your backend API URL:*
    ```
    REACT_APP_BACKEND_URL="http://localhost:5000" # Or your deployed backend URL
    ```

### Running the Application

1.  **Run the Backend (from the `backend` directory):**
    ```bash
    flask run
    ```
    The backend will typically run on `http://localhost:5000`.

2.  **Run the Frontend (from the `frontend` directory):**
    ```bash
    npm start # Or `yarn start`
    ```
    The frontend will typically open in your browser at `http://localhost:3000`.

## 🧪 Testing

The application has undergone thorough testing across various dimensions, including accuracy, response time, and UI responsiveness.

### Experimental Setup:
* **Processor**: Intel Core i7 (11th Gen)
* **RAM**: 16 GB
* **OS**: Windows 11 / Ubuntu 22.04
* **Browser**: Google Chrome v123+
* **Internet**: High-speed connection (minimum 100 Mbps)
* **Deployment Platforms**: Vercel (Frontend), Railway (Flask Backend), Replicate, Gemini, HuggingFace (AI APIs).
* **Test Data**: 15 sample resumes (PDF/TXT), 20 image generation prompts, 5 custom face images, 6 video generation prompts.

### Performance Highlights:
* **Portfolio Website Generator**:
    * Resume parsing accuracy: ~92% (especially for structured PDFs).
    * Upload to website preview time: ~12-15 seconds (average).
* **Image Generation**:
    * Output alignment with prompt intent: 90%.
    * Face likeness: ~85%.
    * Latency: ~20-25 seconds (model complexity dependent).
* **Video Generation**:
    * Video resolution: 720p (15-30 sec clips).
    * Generation time: 45-90 seconds.
* **UI & Authentication**:
    * Secure login/signup with bcrypt hashing: 100% in test cases.
    * Responsive design: No layout issues across devices.
    * Gallery & Dashboard Load Time: < 2 seconds.

## 🛣️ Future Scope

While the AI Super App is already a robust platform, there are exciting avenues for future development:

* **Expanded Document Support**: Include `.docx` resume parsing and support for other document types.
* **Multilingual Capabilities**: Add multilingual support for resume parsing and AI prompts via translation APIs.
* **Custom Domain Deployment**: Allow users to deploy generated portfolio websites to custom domains (e.g., `yourname.superapp.com`).
* **In-App Portfolio Theme Editor**: Enable direct editing of portfolio themes within the application.
* **New AI Asset Generation**: Support for AI-generated logos, posters, and business cards.
* **Portfolio Website Analytics**: Integrate real-time analytics and tracking for generated portfolio websites (e.g., visitor count).
* **Advanced Video Generation Pipeline**: Utilize more advanced models and GPU acceleration for an even more comprehensive video generation experience.
* **AI Summarization & Enhancement Tools**: Integrate AI tools to summarize and enhance uploaded resumes or project content.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement".
Don't forget to give the project a star! ⭐ Thanks!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Alok Agarwal
Shashank Kumar Singh

Project Link: [https://github.com/alokagarwal565/AI-Super-App](https://github.com/alokagarwal565/AI-Super-App)
