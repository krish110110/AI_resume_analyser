# AI Resume Analyzer & ATS Scoring System

A full-stack AI-powered resume analysis and Applicant Tracking System (ATS) scoring platform with role-based access control, FastAPI backend, MongoDB database, and ML-powered analysis pipeline.

## Features

- **User Authentication & Authorization**: Secure login/registration with role-based access (User/Admin)
- **Resume Upload & Parsing**: Support for PDF and DOCX formats
- **AI-Powered Analysis**: Skill extraction, education detection, experience parsing
- **ATS Scoring**: Predict ATS compatibility scores with explanations
- **Job Description Matching**: Compare resumes against job descriptions with similarity scoring
- **Skill Gap Analysis**: Identify missing skills and provide learning resources
- **Interview Preparation**: Generate relevant interview questions based on resume and job description
- **Admin Dashboard**: User management, resume oversight, analytics, and ML model management
- **Interactive Reports**: Visual charts and detailed analysis reports

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB (Motor async driver)
- **Authentication**: JWT with bcrypt
- **ML/AI**: scikit-learn, spaCy, FAISS, Sentence-Transformers
- **File Processing**: PyMuPDF, python-docx

### Frontend
- **Vanilla HTML/CSS/JavaScript**
- **Chart.js** for data visualization
- **Responsive design** with custom CSS

### ML Pipeline
- **Skill Extraction**: Named Entity Recognition + NLP patterns
- **Classification**: Resume category and quality classifiers
- **Similarity**: Sentence-transformers + FAISS vector search
- **ATS Scoring**: Trained predictor models

## Project Structure

```
AI-Resume-Analyzer/
├── frontend/           # Static frontend (HTML/CSS/JS)
├── backend/            # FastAPI backend application
│   └── app/
│       ├── api/        # API routes
│       ├── core/       # Configuration, security, database
│       ├── schemas/    # Pydantic models
│       ├── models/     # MongoDB ODM models
│       ├── repositories/  # Data access layer
│       ├── services/   # Business logic
│       ├── ai/         # ML pipeline modules
│       ├── utils/      # Helper utilities
│       └── tests/      # Backend tests
├── ml/                 # ML training, evaluation, artifacts
├── storage/            # File uploads and generated reports
└── docs/               # Documentation
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js (for frontend development server, optional)
- MongoDB
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-Resume-Analyzer
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python scripts/initialize_database.py
```

5. Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

6. Serve the frontend (optional):
```bash
cd frontend
python -m http.server 3000
# Or use any static file server
```

### Using Docker

```bash
docker-compose up --build
```

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## Environment Variables

See `.env.example` for required environment variables.

## Installation & setup guide

## Getting Started

Follow the instructions below to install and run the AI Resume Analyzer project on Windows, macOS, and Linux.

### Prerequisites

Before running the project, make sure you have installed:

- Python 3.9 or higher
- MongoDB (Local MongoDB or MongoDB Atlas)
- Git
- VS Code or any preferred code editor
- Node.js (Optional)

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Resume-Analyzer
```

## 2. Backend Setup

The backend is developed using FastAPI and MongoDB.

### Windows Installation

**Step 1: Open the backend directory**

```powershell
cd C:\AI-Resume-Analyzer\backend
```

**Step 2: Create a virtual environment**

```powershell
python -m venv venv
```

**Step 3: Activate the virtual environment**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

**Step 4: Install dependencies**

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Step 5: Configure environment variables**

```powershell
Copy-Item .env.example .env
```

Open the `.env` file and configure the required environment variables, such as MongoDB connection URL, JWT secret key, and other application settings.

**Step 6: Initialize the database**

```powershell
python scripts/initialize_database.py
```

**Step 7: Run the FastAPI backend**

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend URL:

`http://localhost:8000`

---

### macOS / Linux Installation

**Step 1: Open the backend directory**

```bash
cd AI-Resume-Analyzer/backend
```

**Step 2: Create a virtual environment**

```bash
python3 -m venv venv
```

**Step 3: Activate the virtual environment**

For macOS / Linux:

```bash
source venv/bin/activate
```

**Step 4: Install dependencies**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Step 5: Configure environment variables**

```bash
cp .env.example .env
```

Edit the `.env` file and configure the required application settings.

**Step 6: Initialize the database**

```bash
python scripts/initialize_database.py
```

**Step 7: Run the FastAPI backend**

```bash
uvicorn app.main:app --reload --port 8000
```

Backend URL:

`http://localhost:8000`

---

## 3. Frontend Setup

The frontend uses HTML, CSS, Vanilla JavaScript, and Chart.js.

Keep the backend running and open a **new terminal**.

### Windows

```powershell
cd C:\AI-Resume-Analyzer\frontend
python -m http.server 3000
```

### macOS / Linux

```bash
cd AI-Resume-Analyzer/frontend
python3 -m http.server 3000
```

Frontend URL:

`http://localhost:3000`

---

## 4. API Documentation

After starting the backend, access the interactive API documentation.

- **Swagger UI:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc

---

## 5. Running the Project

To run the complete application, follow these steps:

1. Start MongoDB or configure your MongoDB Atlas connection.
2. Open the first terminal and start the FastAPI backend.
3. Open the second terminal and start the frontend server.
4. Open your browser and visit `http://localhost:3000`.
5. Register or log in to access the AI Resume Analyzer features.

### Important Notes

- Always activate the Python virtual environment before running backend commands.
- Make sure MongoDB is running and the connection URL is correctly configured.
- Never upload your `.env` file or secret credentials to GitHub.
- The backend and frontend must run simultaneously.
- Use `Ctrl + C` to stop the running servers.
- The `venv` folder should not be committed to GitHub.

---

## 6. Docker Installation (Optional)

If Docker and Docker Compose are configured:

```bash
docker-compose up --build
```

To stop the containers:

```bash
docker-compose down
```

## License

MIT License


backen running commande:-  cd C:\AI-Resume-Analyzer\backend
environment turn on :-  .\venv\Scripts\Activate.ps1

frontend running command :-cd C:\AI-Resume-Analyzer\frontend
python -m http.server 3000
