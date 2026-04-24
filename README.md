# Aura Health AI - Disease Prediction Chatbot

Aura Health AI is a full-stack web application based on the research paper *"Health Chatbot Using Natural Language Processing for Disease Prediction and Treatment"*. It utilizes Natural Language Processing (NLP) to understand user symptoms described in simple English and predicts potential diseases along with their recommended treatments.

## 🌟 Features

- **Dual Modes:**
  - **"I know my disease"**: Direct treatment lookup for known conditions.
  - **"I want to check my symptoms"**: NLP-based symptom analysis to predict underlying conditions.
- **Natural Language Processing**: Built with `nltk` and `scikit-learn` using Tokenization, Stopword Removal, Lemmatization, and Cosine Similarity.
- **Simple English Support**: Optimized to understand colloquial terms and everyday language.
- **Premium UI/UX**: Designed with modern glassmorphism, dynamic gradients, smooth micro-animations, and responsive layouts.
- **Quick Actions**: Built-in symptom chips for faster typing and interaction.

---

## 🛠️ Tech Stack

- **Frontend**: React.js, Vite, Vanilla CSS (Glassmorphism design)
- **Backend**: Python, FastAPI, Uvicorn
- **Machine Learning**: `scikit-learn` (TF-IDF Vectorization, Cosine Similarity), `nltk` (Text preprocessing)

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites
- Node.js (v18+)
- Python (3.9+)

### 1. Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```
   *The API will be available at http://localhost:8000*

### 2. Frontend Setup (React + Vite)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The application will be available at http://localhost:5173*

---

## 🧠 How it Works (NLP Pipeline)

1. **Preprocessing**: The user's simple English input is converted to lowercase, tokenized, and stripped of punctuation and common English stopwords (e.g., "the", "is", "at").
2. **Lemmatization**: Words are reduced to their root form (e.g., "running" -> "run", "hurts" -> "hurt") to improve matching accuracy.
3. **Vectorization**: The processed input is converted into a numerical format using `TF-IDF` (Term Frequency-Inverse Document Frequency).
4. **Similarity Scoring**: `Cosine Similarity` is calculated between the user's input vector and the vectors of all known symptoms in the database.
5. **Prediction**: The disease associated with the symptom that has the highest similarity score (above a dynamic threshold) is returned to the user with a treatment plan.

---

## 📝 Disclaimer
This application is designed for educational and informational purposes only. The AI predictions are not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.
