# 🗳️ Interactive Election Assistant

A production-ready, accessible, and intelligent AI assistant designed to help users navigate the election process, understand registration steps, and track important timelines. Built for the **PromptWar Hackathon 2026**.

## 🚀 Key Features
- **Intelligent Guidance**: Powered by **Gemini 3 Flash** via the unified Google GenAI SDK.
- **Stateful Conversation**: Uses **LangGraph** for robust conversation state management.
- **Modern UI/UX**: Built with **React 19**, **TailwindCSS**, and **Lucide React** icons.
- **Production Ready**: Modular backend using **FastAPI** and **uv** for performance-optimized environment management.
- **Accessibility**: Semantic HTML and ARIA-compliant chat interface.

---

## 🛠️ Tech Stack
- **Frontend**: Vite + React (TypeScript) + TailwindCSS
- **Backend**: FastAPI + LangGraph + google-genai
- **Environment Management**: uv
- **Deployment**: Google Cloud Run

---

## 🏗️ Local Development

### 1. Prerequisites
- Install **uv** (Python package manager): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Node.js (v18+)

### 2. Backend Setup
```bash
cd backend
# Create .env file with your GOOGLE_API_KEY
uv run uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## ☁️ Deployment Guide (Google Cloud Run)

To deploy this project to Google Cloud Run, follow these steps:

### 1. Build and Push Backend Image
```bash
cd backend
gcloud builds submit --tag gcr.io/[PROJECT_ID]/election-assistant-backend
```

### 2. Deploy to Cloud Run
```bash
gcloud run deploy election-assistant-backend \
  --image gcr.io/[PROJECT_ID]/election-assistant-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=[YOUR_API_KEY],GOOGLE_PROJECT_ID=[YOUR_PROJECT_ID]
```

### 3. Frontend Deployment
Build the frontend and host it on Firebase Hosting or Vercel:
```bash
cd frontend
npm run build
```

---

## ⚖️ Neutrality & Guardrails
The assistant is strictly constrained by a system prompt to:
1. Remain neutral and unbiased.
2. Redirect non-election queries back to the core topic.
3. Provide step-by-step verified election procedures.

---

**Developed for the PromptWar Hackathon - May 2026**
