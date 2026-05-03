# Election Assistant - 2-Hour Hackathon Implementation Plan

Given the strict 2-hour time constraint and the requirement for a production-ready, modular architecture, we need to focus on delivering a robust MVP (Minimum Viable Product). We will build a focused React frontend communicating with a FastAPI backend powered by LangGraph and Gemini.

## Tech Stack Overview
*   **Environment Manager:** `uv` (Python 3.12.x)
*   **Backend:** FastAPI, Uvicorn
*   **AI Framework:** LangChain, LangGraph, Google GenAI (Gemini)
*   **Frontend:** React (via Vite) + TypeScript (optional, but good for stability) or JavaScript
*   **Styling:** TailwindCSS (for rapid, premium UI development)

---

## Timeline Breakdown (120 Minutes)

### Phase 1: Environment Setup & Scaffolding (15 Minutes)
**Goal:** Have both backend and frontend environments initialized and running.
*   **Backend (`/backend`):**
    *   Initialize python environment using `uv`.
    *   Install dependencies: `fastapi`, `uvicorn`, `langchain`, `langgraph`, `pydantic`, `google-genai`.
    *   Set up a modular folder structure (`routers`, `services`, `agent`, `models`, `utils`).
*   **Frontend (`/frontend`):**
    *   Initialize Vite React project.
    *   Install TailwindCSS or a fast component library (like Lucide React for icons).

### Phase 2: Backend Core - LangGraph & FastAPI (45 Minutes)
**Goal:** Build the agentic logic and expose it via a REST endpoint.
*   **Agent Construction (`/backend/agent`):**
    *   Define the `AgentState` (messages list, current topic).
    *   Create a simple LangGraph with an entry node calling Gemini with an "Election Expert" system prompt.
    *   (Optional if time permits) Add a tool/node for retrieving specific election dates from a mock database or document.
*   **API Development (`/backend/routers`):**
    *   Create a POST `/api/chat` endpoint.
    *   Integrate the compiled LangGraph to stream or return responses.
    *   Implement basic error handling (try/catch blocks, HTTP exceptions) and logging.

### Phase 3: Frontend Core - Chat Interface (40 Minutes)
**Goal:** Build a premium, interactive chat UI.
*   **Components (`/frontend/src/components`):**
    *   `ChatInterface`: Main container.
    *   `MessageBubble`: To display user vs. AI messages.
    *   `ChatInput`: Text area with a submit button.
*   **State Management:**
    *   Manage message history and loading states.
*   **Integration:**
    *   Connect the UI to the FastAPI backend using `fetch` or `axios`.
*   **Styling:**
    *   Apply a clean, modern design (e.g., a centered chat window with subtle shadows and clear typography).

### Phase 4: Polish, Testing, and Documentation (20 Minutes)
**Goal:** Meet the production-ready and documentation requirements.
*   **Code Quality:** Add docstrings and type hints to Python functions. Ensure React components are clean.
*   **Error Handling & Logging:** Ensure the backend logs requests and errors properly. Show user-friendly error messages on the frontend.
*   **Documentation:** Create a concise `README.md` with instructions on how to start both servers concurrently.
*   **Final Review:** Test the end-to-end flow to ensure the agent correctly answers questions about the election process.

---

## Proposed Folder Structure
```text
.
├── backend/
│   ├── app/
│   │   ├── agent/          # LangGraph logic, prompts, nodes
│   │   ├── api/            # FastAPI routers
│   │   ├── core/           # Config, logging setup
│   │   ├── models/         # Pydantic schemas
│   │   └── main.py         # FastAPI application instance
│   ├── .env                # API Keys
│   └── pyproject.toml      # uv dependencies
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── services/       # API call logic
    │   ├── App.jsx         # Main React app
    │   └── index.css       # Global styles
    └── package.json
```

## Strategy for Success in 2 Hours
1.  **Hardcode Context First:** Instead of setting up a complex RAG pipeline, we will start by injecting the election process context directly into the Gemini System Prompt. If time permits, we can upgrade it to a tool-based retrieval system.
2.  **Iterative Delivery:** We will build a working pipeline first (UI -> API -> Simple LLM response), and then enhance the LLM logic into a LangGraph in the second iteration.
3.  **Minimize Boilerplate:** Use Vite for React and standard FastAPI patterns.
