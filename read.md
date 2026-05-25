 # Task Manager DBMS

A simple task management web application with a FastAPI backend and a Streamlit frontend.

## Project Overview
- **Purpose:** Demonstration project for managing tasks (create, read, update, delete) backed by a lightweight API.
- **Backend:** FastAPI app in `backend/main.py` with dependencies listed in `backend/requirements.txt`.
- **Frontend:** Streamlit UI in `frontend/app.py` and an API helper in `frontend/api_service.py`.

## Features
- Create, view, update, and delete tasks via REST API.
- Streamlit-based frontend that interacts with the backend API.
- Simple, easy-to-run local development setup.

## Architecture
- `backend/` — FastAPI application and requirements.
- `frontend/` — Streamlit UI and API service code.

## Prerequisites
- Python 3.10 or newer
- pip

## Setup (Windows)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install backend dependencies:

```powershell
cd backend
pip install -r requirements.txt
cd ..
```

3. Install frontend dependencies (if not included in backend requirements):

```powershell
pip install streamlit requests
```

## Running the app
- Start the backend (assumes FastAPI `app` in `backend/main.py`):

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

- Start the frontend (Streamlit):

```powershell
cd ../frontend
streamlit run app.py
```

The frontend communicates with the backend at `http://localhost:8000` by default.

## Project Structure
```
task_manager_DBMS/
  backend/
    main.py
    requirements.txt
  frontend/
    api_service.py
    app.py
  read.md
```

## Contributing
- Open an issue or submit a PR with improvements.
- Keep changes minimal and add tests where appropriate.

## License
This project is provided as-is for learning and demonstration purposes.
