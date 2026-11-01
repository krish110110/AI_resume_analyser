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

## License

MIT License




backen running commande:-  cd C:\AI-Resume-Analyzer\backend
environment turn on :-  .\venv\Scripts\Activate.ps1



frontend running command :-cd C:\AI-Resume-Analyzer\frontend
python -m http.server 3000