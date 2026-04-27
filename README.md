# 🚀 AI Super App: The Ultimate Creative Suite

The **AI Super App** is a high-performance, all-in-one creativity platform powered by the world's most advanced generative models. Built for creators, developers, and visionaries, it merges cinematic video synthesis, high-fidelity image generation, intelligent document interaction (RAG), and strategic thinking into a single, unified experience.

---

## 🌟 Core Modules

### 🎨 AI Image Studio (Powered by Gemini 3.1)
Generate breathtaking 4K visuals with professional-grade controls.
*   **Deep Thinking (Reasoning)**: Enable AI to "think" before drawing for superior composition.
*   **Dual Grounding**: Enhance generation with live Web and Image search data.
*   **Pro Controls**: Customizable aspect ratios (16:9, 9:16, 1:1, 4:3) and resolutions up to 4K.
*   **Reference Input**: Upload existing assets to maintain character or style consistency.

### 🎬 AI Video Studio (Powered by VEO 3.1)
Transform prompts into cinematic temporal masterpieces.
*   **VEO 3.1 Engine**: Next-generation video synthesis with improved motion and consistency.
*   **Keyframe Interpolation**: Provide start/end frames; the AI generates the motion between them.
*   **Temporal Grounding**: Maintain consistency across complex cinematic sequences.

### 📁 AI Document RAG (Knowledge Bases)
Interact with your data using advanced Retrieval-Augmented Generation.
*   **Enterprise Knowledge Base**: Secure, multi-user document analysis for teams.
*   **Personal Knowledge Base**: Private, local-first data interaction for individual researchers.
*   **Deep Insights**: Extract summaries, find contradictions, and chat with complex datasets.

### 🌐 AI Portfolio Builder (Next.js 15 + Gemini 3.1 Pro)
Generate a pixel-perfect portfolio website instantly from your resume.
*   **Instant Synthesis**: Converts raw text/PDF into a responsive Tailwind CSS site.
*   **Refined Layouts**: Uses Gemini 3.1 Pro Preview for superior design reasoning.
*   **Live Customization**: Real-time editing and deployment-ready code generation.

### 🧠 AI Thinking-to-Content Engine
A strategic planning tool designed to prevent AI repetition and improve content quality.
*   **Idea Refinement**: Capture raw thoughts and structure them into mind maps.
*   **Planning-First**: AI plans the content structure before generation.
*   **Platform-Ready**: Output tailored for LinkedIn, X, Blogs, or Technical Whitepapers.

### 🏗️ AI Multi-App Workspace
A voice/natural-language-controlled unified workspace.
*   **Universal Command**: Control a drawing canvas, task manager, and layout builder via text or voice.
*   **Real-time Collaboration**: Synchronized workspace for team-based AI orchestration.

---

## 🛠️ Technology Stack

### Frontend & Design
*   **Next.js 15 & React**: Powers the high-performance Portfolio Builder and Workspace.
*   **Flask (Jinja2)**: Core dashboard and studio routing.
*   **Premium Vanilla CSS**: A custom-built design system featuring glassmorphism, cinematic blurs, and micro-animations.
*   **Tailwind CSS**: Utility-first styling for the generated portfolio sites.

### Backend & AI
*   **Python (Flask)**: Primary backend handler for studio logic and model orchestration.
*   **Gemini 3.1 / VEO 3.1 API**: Core intelligence layer for image, video, and reasoning tasks.
*   **SQLAlchemy**: Secure user authentication and asset management (AI Vault).
*   **Subprocess Orchestration**: Manages concurrent Node.js and Python microservices.

### Database
*   **SQLite / PostgreSQL**: Relational data storage for user credentials and metadata.

---

## 🏗️ Architecture

The AI Super App follows a **Modular Micro-Hub Architecture**. Each studio (Image, Video, RAG, Portfolio) operates as a specialized node that shares a centralized authentication and credit system, ensuring a seamless flow between different creative tasks.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+ (for Portfolio Builder & Workspace)
*   Google Gemini API Key

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/alokagarwal565/AI-Super-App.git
    cd ai-super-app
    ```

2.  **Setup Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_key_here
    SECRET_KEY=your_flask_secret
    ```

4.  **Run the App**:
    ```bash
    python app.py
    ```

---

## 🔒 Security & Privacy
*   **Bcrypt Authentication**: Industry-standard password hashing.
*   **Local Vault**: Assets are stored securely and associated with unique user IDs.
*   **Data Isolation**: Personal Knowledge Bases in the RAG module are isolated for maximum privacy.

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for the next generation of creators.
