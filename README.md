# 🩺 Healthcare Symptom Checker

An AI-powered web app that analyzes user-described symptoms and provides possible conditions and next steps (for educational purposes only).
Built using **FastAPI**, **React + Vite**, and **Groq LLMs**.

---

## Project features

- **LLM-Powered Diagnosis** — Uses Groq’s LLaMA / Mixtral models for symptom analysis
- **Educational, Non-Diagnostic Output** — Always includes disclaimers
- **SQLite Database Logging** — Saves all analyses and timestamps
- **Search & Filter History** — Quickly look up previous entries
- **Delete / Clear History** — Manage your stored records easily
- **FastAPI + React Stack** — Clean architecture and responsive UI

---

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React + Vite, Axios, React-Markdown |
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **LLM** | Groq API (LLaMA-3.1 / Mixtral-8x7B) |
| **Database** | SQLite |
| **Styling** | Custom CSS (Dark UI with cyan + red accents) |

---

## Sample Screenshot

<img width="725" height="570" alt="image" src="https://github.com/user-attachments/assets/9368bd9a-15d3-45aa-a997-29467dd0b651" />

## Sample Output

<img width="637" height="769" alt="image" src="https://github.com/user-attachments/assets/1c9ce83a-8861-48a7-8a8c-768981fceaed" />

## Setup Guide

### 1) Clone the Repository
```bash
git clone https://github.com/<your-username>/healthcare-symptom-checker.git
cd healthcare-symptom-checker
```

### 2️) Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install fastapi uvicorn sqlalchemy python-dotenv groq pydantic
```

#### Create `.env`
```
GROQ_API_KEY=your_groq_api_key_here
```

#### Run Backend
```bash
uvicorn app:app --reload
```
API runs at → `http://127.0.0.1:8000`

---

### 3️) Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at → `http://localhost:5173`

---

## Example Usage

1. Open the React app
2. Describe your symptoms (e.g., *"I have a sore throat and mild fever"*)
3. Click **Analyze**
4. View AI diagnosis + recommended next steps
5. Search or delete entries anytime

---

## API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/analyze` | Analyze given symptom text using Groq LLM |
| `GET` | `/history` | Retrieve all saved analyses (optional keyword filter) |
| `DELETE` | `/history/{id}` | Delete a specific record |
| `DELETE` | `/history` | Clear all records |

---

---

## AI Models Used

The app dynamically selects from available models:
- `mixtral-8x7b-32768` → High-context reasoning
- `llama-3.1-70b-versatile` → Balanced reasoning and speed
- `llama-3.1-8b-instant` → Fast fallback

If one fails, the app automatically retries with the next.

---

---

## ⚠️ Disclaimer

This app is **for educational and informational purposes only**.
It does **not** provide medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional for medical concerns.

---
