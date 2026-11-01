
# AI Resume Analyzer & ATS Scoring System — Project Details

## 1. Project Overview

This is a full-stack AI-powered resume analysis and Applicant Tracking System (ATS) scoring platform. It allows users to upload resumes (PDF/DOCX), analyze them against job descriptions, get ATS compatibility scores, identify missing skills, and view detailed reports with visual charts. Admins can manage users, view all reports, and monitor platform analytics.

### Core Functionalities
- **User Authentication & Authorization**: Secure login/registration with role-based access (User/Admin)
- **Resume Upload & Parsing**: Support for PDF and DOCX formats
- **AI-Powered Analysis**: Skill extraction, education detection, experience parsing, project extraction, certification extraction
- **ATS Scoring**: Predict ATS compatibility scores with explanations
- **Job Description Matching**: Compare resumes against job descriptions with similarity scoring
- **Skill Gap Analysis**: Identify missing skills and provide learning resources
- **Interview Preparation**: Generate relevant interview questions based on resume and job description
- **Admin Dashboard**: User management, report oversight, analytics, and ML model management
- **Interactive Reports**: Visual charts and detailed analysis reports

---

## 2. Languages Used

### Backend
| Language/Framework | Purpose |
|-------------------|---------|
| **Python 3.9+** | Primary backend language |
| **FastAPI** | Web framework for API endpoints |
| **MongoDB + Motor** | NoSQL database with async driver |
| **JWT (python-jose)** | Authentication tokens |
| **bcrypt (passlib)** | Password hashing |

### Frontend
| Language/Framework | Purpose |
|-------------------|---------|
| **HTML5** | Page structure |
| **CSS3** | Styling (no framework, custom CSS) |
| **JavaScript (ES6+)** | Frontend logic (no framework, vanilla JS) |
| **Chart.js v4.4.7** | Data visualization charts |

### ML/AI
| Language/Library | Purpose |
|------------------|---------|
| **Python** | ML training and inference |
| **scikit-learn** | Traditional ML models |
| **spaCy** | NLP processing |
| **Sentence-Transformers** | Text embeddings for similarity |
| **FAISS** | Vector search for similarity matching |
| **PyMuPDF** | PDF text extraction |
| **python-docx** | DOCX text extraction |

---

## 3. ML Models: ATS Score and Missing Skills

### Current Implementation Status
**Important**: The backend AI layer currently contains **stub implementations** that return randomized or rule-based results. The actual trained ML models have not been deployed yet. The `ml/artifacts/` directories are empty. However, the intended model architectures are fully documented in training scripts.

---

### ATS Score Prediction Model

| Attribute | Details |
|-----------|---------|
| **Purpose** | Predict ATS (Applicant Tracking System) compatibility score for a resume |
| **Intended Algorithm** | `LinearRegression` (scikit-learn) |
| **Input Features** | Resume text + Job description text |
| **Output** | ATS compatibility score (float, 0-100) + verdict |
| **Training Script** | `ml/training/train_ats_predictor.py` |
| **Current Status** | Stub — returns `random.uniform(50, 95)` |
| **Planned Artifacts** | `ml/artifacts/ats_predictor/` (empty) |

**How it should work**:
1. Resume text and job description are preprocessed
2. Features are extracted (skills match, keyword density, section presence, etc.)
3. LinearRegression model predicts ATS score
4. Score is returned with breakdown and recommendations

---

### Missing Skill Detection

| Attribute | Details |
|-----------|---------|
| **Purpose** | Identify skills present in job description but missing from resume |
| **Algorithm** | Set difference: `job_skills - resume_skills` |
| **Input** | Resume skills list + Job description skills list |
| **Output** | List of missing skills |
| **Implementation** | Functional but rule-based |
| **File** | `backend/app/ai/skills/missing_skill_detector.py` |

**How it works**:
1. Skills are extracted from resume using keyword matching
2. Skills are extracted from job description
3. Missing skills = job skills not found in resume skills
4. Returns list of missing keywords with suggestions

---

### Skill Extraction Model

| Attribute | Details |
|-----------|---------|
| **Purpose** | Extract technical and professional skills from resume text |
| **Intended Algorithm** | `CountVectorizer` + `MultinomialNB` (Naive Bayes) |
| **Input** | Raw resume text |
| **Output** | List of extracted skill labels |
| **Training Script** | `ml/training/train_skill_extractor.py` |
| **Training Data** | `ml/datasets/raw/resumes.csv` and `ml/datasets/raw/jobs.csv` |
| **Current Status** | Stub — uses hardcoded substring matching against a predefined skills list |
| **File** | `backend/app/ai/skills/skill_matcher.py` |

**Current implementation**: Simple case-insensitive substring matching against a hardcoded list of ~50 common skills (python, java, javascript, react, node.js, sql, aws, docker, etc.)

---

### Resume Classification Model

| Attribute | Details |
|-----------|---------|
| **Purpose** | Classify resume into category and seniority level |
| **Intended Algorithm** | `RandomForestClassifier` (scikit-learn) |
| **Input** | Resume text |
| **Output** | Category (Software Engineering, Data Science, etc.) + Level (Junior, Mid, Senior, Lead, Executive) |
| **Training Script** | `ml/training/train_classifier.py` |
| **Current Status** | Stub — returns random category/seniority |
| **File** | `backend/app/ai/classification/resume_classifier.py` |

---

### Quality Classification Model

| Attribute | Details |
|-----------|---------|
| **Purpose** | Evaluate resume quality and identify issues |
| **Intended Algorithm** | `RandomForestClassifier` (scikit-learn) |
| **Input** | Resume text |
| **Output** | Quality score (float, 0-100) + list of issues |
| **Training Script** | `ml/training/train_quality_classifier.py` |
| **Current Status** | Stub — returns random quality score |
| **File** | `backend/app/ai/classification/quality_classifier.py` |

---

### Similarity Model

| Attribute | Details |
|-----------|---------|
| **Purpose** | Calculate similarity between resume and job description |
| **Intended Algorithm** | Sentence Transformers embeddings + FAISS vector search |
| **Input** | Resume text + Job description text |
| **Output** | Similarity score (float, 0-100) |
| **Current Status** | Stub — returns `random.uniform(40, 90)` |
| **File** | `backend/app/ai/similarity/similarity_service.py` |

---

## 4. Complete Tech Stack

### Backend Stack
| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI 0.104.1 |
| **Server** | Uvicorn 0.24.0 |
| **Database** | MongoDB 7.0 (Motor 3.3.2 async driver) |
| **Authentication** | JWT (python-jose 3.3.0) + bcrypt (passlib 1.7.4) |
| **Validation** | Pydantic 2.5.0 + pydantic-settings 2.1.0 |
| **File Upload** | python-multipart 0.0.6 |
| **PDF Extraction** | PyMuPDF 1.23.8 |
| **DOCX Extraction** | python-docx 1.1.0 |
| **ML/AI** | scikit-learn 1.3.2, sentence-transformers 2.2.2, faiss-cpu 1.8.0 |
| **NLP** | spacy 3.7.2 |
| **Data Processing** | numpy 1.26.2, pandas 2.1.4 |
| **Image Processing** | pillow 10.1.0 |
| **HTTP Client** | requests 2.31.0, httpx 0.25.2 |
| **Config** | python-dotenv 1.0.0 |
| **Date/Time** | python-dateutil 2.8.2 |
| **Retry Logic** | tenacity 8.2.3 |
| **Testing** | pytest 7.4.3, pytest-asyncio 0.21.1 |
| **Code Quality** | black 23.12.0, ruff 0.1.9, mypy 1.7.1 |

### Frontend Stack
| Component | Technology |
|-----------|-----------|
| **Structure** | Vanilla HTML5 |
| **Styling** | Custom CSS3 (no framework) |
| **Logic** | Vanilla JavaScript ES6+ (no framework) |
| **Charts** | Chart.js 4.4.7 |
| **Fonts** | Google Fonts (Inter) |
| **Icons** | Emoji (no icon library) |
| **Build Tools** | None — served as static files |

---

## 5. Project Architecture

### Backend Architecture
```
backend/app/
├── main.py                    # FastAPI app entry point
├── api/v1/
│   ├── router.py              # Main API router
│   ├── auth.py                # Authentication endpoints
│   ├── users.py               # User management endpoints
│   ├── admin.py               # Admin endpoints (stats, users, reports, analytics)
│   ├── resume.py              # Resume upload/list/delete endpoints
│   ├── analysis.py            # Analysis creation/retrieval
│   ├── job_description.py     # Job description CRUD
│   ├── reports.py             # Report listing and retrieval
│   ├── dashboard.py           # Dashboard stats endpoints
│   └── health.py              # Health check endpoint
├── core/
│   ├── config.py              # Settings and environment config
│   ├── security.py            # JWT token creation/verification
│   ├── database.py            # MongoDB connection
│   └── constants.py           # App constants
├── models/
│   ├── user.py                # User MongoDB model
│   ├── resume.py              # Resume MongoDB model
│   ├── analysis.py            # Analysis MongoDB model
│   ├── report.py              # Report MongoDB model
│   └── job_description.py     # Job description MongoDB model
├── schemas/                   # Pydantic request/response models
├── repositories/              # Data access layer
│   ├── user_repository.py
│   ├── resume_repository.py
│   ├── analysis_repository.py
│   ├── report_repository.py
│   └── job_description_repository.py
├── services/                  # Business logic layer
│   ├── auth_service.py
│   ├── user_service.py
│   ├── resume_service.py      # Resume processing orchestration
│   ├── analysis_service.py
│   ├── report_service.py
│   ├── dashboard_service.py
│   └── job_description_service.py
├── ai/                        # ML Pipeline
│   ├── pipeline/
│   │   └── analysis_pipeline.py   # Main orchestrator
│   ├── parsing/
│   │   ├── text_cleaner.py
│   │   ├── section_detector.py
│   │   └── resume_parser.py
│   ├── extraction/
│   │   ├── skill_extractor.py
│   │   ├── education_extractor.py
│   │   ├── experience_extractor.py
│   │   ├── project_extractor.py
│   │   └── certification_extractor.py
│   ├── classification/
│   │   ├── resume_classifier.py
│   │   └── quality_classifier.py
│   ├── scoring/
│   │   ├── ats_scorer.py
│   │   ├── similarity_scorer.py
│   │   └── skill_match_scorer.py
│   ├── skills/
│   │   ├── skill_matcher.py
│   │   └── missing_skill_detector.py
│   ├── similarity/
│   │   └── similarity_service.py
│   ├── recommendations/
│   │   ├── suggestion_generator.py
│   │   └── resource_retriever.py
│   └── interview/
│       ├── question_generator.py
│       └── question_retriever.py
├── utils/                     # Helper utilities
│   ├── pdf_extractor.py
│   ├── docx_extractor.py
│   └── text_utils.py
└── tests/                     # Backend tests
```

### ML Pipeline Flow
```
Resume Upload
    ↓
PDF/DOCX Text Extraction
    ↓
Text Cleaning & Section Detection
    ↓
Feature Extraction (Skills, Education, Experience, Projects, Certifications)
    ↓
Classification (Category, Level, Quality)
    ↓
Scoring (ATS Score, Similarity, Skill Match, Missing Keywords)
    ↓
Recommendations Generation
    ↓
Report Creation & Storage
```

### Frontend Architecture
```
frontend/
├── index.html                          # Public landing page
├── css/
│   ├── global.css                      # Design tokens, utilities, animations
│   ├── auth.css                        # Login/register forms
│   ├── admin-dashboard.css             # Admin layout, sidebar, tables
│   ├── user-dashboard.css              # User sidebar, stat cards, upload
│   ├── report.css                      # Report display, score circles
│   └── upload.css                      # Upload zone, progress bar
├── js/
│   ├── chart.min.js                    # Chart.js v4.4.7
│   ├── config.js                       # API config, token helpers
│   ├── api.js                          # Centralized API service
│   ├── common.js                       # Shared utilities
│   ├── auth/
│   │   ├── login.js
│   │   ├── register.js
│   │   ├── logout.js
│   │   └── auth-guard.js
│   ├── user/
│   │   ├── dashboard.js
│   │   ├── upload.js
│   │   ├── report.js
│   │   ├── history.js
│   │   └── profile.js
│   ├── admin/
│   │   ├── dashboard.js
│   │   ├── users.js
│   │   ├── reports.js
│   │   ├── analytics.js
│   │   └── models.js
│   └── charts/
│       ├── dashboard-charts.js
│       ├── report-charts.js
│       └── admin-charts.js
├── auth/
│   ├── login.html
│   ├── register.html
│   └── forgot-password.html
├── user/
│   ├── dashboard.html
│   ├── upload.html
│   ├── report.html
│   ├── history.html
│   └── profile.html
└── admin/
    ├── dashboard.html
    ├── users.html
    ├── reports.html
    ├── analytics.html
    └── models.html
```

---

## 6. API Endpoints

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/forgot-password` | Request password reset |

### Users
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/users/me` | Get current user profile |
| PUT | `/api/v1/users/me` | Update current user profile |

### Resumes
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/resumes/upload` | Upload resume for analysis |
| GET | `/api/v1/resumes/` | List user's resumes |
| GET | `/api/v1/resumes/{id}` | Get specific resume |
| DELETE | `/api/v1/resumes/{id}` | Delete resume |

### Analysis
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/analysis` | Create new analysis |
| GET | `/api/v1/analysis/{id}` | Get analysis result |

### Reports
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/reports/` | List user's reports |
| GET | `/api/v1/reports/{id}` | Get specific report |
| GET | `/api/v1/reports/by-resume/{resume_id}` | Get report by resume ID |

### Job Descriptions
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/jobs` | Create job description |
| GET | `/api/v1/jobs/` | List job descriptions |
| GET | `/api/v1/jobs/{id}` | Get specific job description |

### Admin
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/admin/stats` | Admin dashboard stats |
| GET | `/api/v1/admin/users` | List all users |
| DELETE | `/api/v1/admin/users/{id}` | Delete user |
| GET | `/api/v1/admin/reports` | List all reports |
| GET | `/api/v1/admin/analytics` | Admin analytics data |

### Dashboard
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/dashboard/user` | User dashboard stats |
| GET | `/api/v1/dashboard/admin` | Admin dashboard stats |

### Health
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | API health check |

---

## 7. Database Models (MongoDB)

### User
- `_id`: ObjectId
- `name`: string
- `email`: string (unique)
- `password`: string (bcrypt hashed)
- `role`: enum (user, admin)
- `is_active`: boolean
- `created_at`: datetime
- `updated_at`: datetime

### Resume
- `_id`: ObjectId
- `user_id`: string
- `filename`: string
- `file_path`: string
- `file_type`: string (pdf, docx)
- `file_size`: int
- `status`: enum (pending, processing, completed, failed)
- `ats_score`: float
- `similarity_score`: float
- `skill_match_percentage`: float
- `missing_keywords`: list[string]
- `created_at`: datetime
- `updated_at`: datetime

### Analysis
- `_id`: ObjectId
- `resume_id`: string
- `job_description_id`: string
- `parsed_data`: dict
- `features`: dict
- `classification`: dict
- `scores`: dict
- `recommendations`: list[string]
- `created_at`: datetime

### Report
- `_id`: ObjectId
- `user_id`: string
- `resume_id`: string
- `analysis_id`: string
- `filename`: string
- `ats_score`: float
- `similarity_score`: float
- `skill_match_percentage`: float
- `skills`: list[string]
- `missing_keywords`: list[string]
- `recommendations`: list[string]
- `parsed_data`: dict
- `features`: dict
- `classification`: dict
- `scores`: dict
- `created_at`: datetime

### Job Description
- `_id`: ObjectId
- `user_id`: string
- `title`: string
- `description`: string
- `skills`: list[string]
- `created_at`: datetime
- `updated_at`: datetime

---

## 8. Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MONGO_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGO_DB_NAME` | Database name | `ai_resume_analyzer` |
| `SECRET_KEY` | JWT signing secret | `super-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `7` |
| `UPLOAD_DIR` | Resume upload directory | `storage/uploads` |
| `REPORTS_DIR` | Generated reports directory | `storage/generated_reports` |
| `MAX_UPLOAD_SIZE_MB` | Max file size | `10` |
| `ALLOWED_EXTENSIONS` | Allowed file types | `pdf,docx` |
| `SPACY_MODEL` | spaCy model name | `en_core_web_sm` |
| `SENTENCE_TRANSFORMER_MODEL` | Sentence transformer model | `all-MiniLM-L6-v2` |
| `FAISS_INDEX_PATH` | FAISS index path | `ml/artifacts/faiss/index.faiss` |
| `ADMIN_EMAIL` | Default admin email | `admin@example.com` |
| `ADMIN_PASSWORD` | Default admin password | `admin123` |
| `ENVIRONMENT` | Environment | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8000` |
| `API_V1_STR` | API prefix | `/api/v1` |

---

## 9. How to Run

### Prerequisites
- Python 3.9+
- MongoDB (running on port 27017)
- Node.js (optional, for frontend dev server)

### Backend
```powershell
cd C:\AI-Resume-Analyzer\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### Frontend
```powershell
cd C:\AI-Resume-Analyzer\frontend
python -m http.server 3000 --bind 0.0.0.0
```

### Access
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/v1/docs`
- Admin login: `admin@example.com` / `admin123`

---

## 10. Current State Summary

| Component | Status |
|-----------|--------|
| Backend API | Fully functional, tests pass (4/4) |
| Frontend UI | Fully functional with responsive design |
| MongoDB Integration | Complete |
| JWT Authentication | Complete |
| Resume Upload/Parsing | Complete (PDF + DOCX) |
| ATS Scoring | **Stub** — returns random scores |
| Skill Extraction | **Stub** — uses hardcoded keyword list |
| Classification | **Stub** — returns random results |
| Similarity Scoring | **Stub** — returns random scores |
| Missing Skill Detection | Functional — set difference logic |
| ML Model Training | Skeleton scripts only, no trained models |
| Model Artifacts | None exist (`ml/artifacts/` is empty) |
| Admin Dashboard | Complete with users, reports, analytics |
| Charts | Chart.js integrated for reports and analytics |
| Docker | `docker-compose.yml` available |

---

## 11. Next Steps for Production

1. Train and serialize actual ML models using `ml/training/` scripts
2. Replace stub implementations in `backend/app/ai/` with trained models
3. Implement actual email sending for forgot-password
4. Add frontend unit tests
5. Add rate limiting and security hardening
6. Add error pages (404, 500)
7. Add mobile hamburger menu for sidebar
8. Add dark/light theme toggle
9. Add export functionality for reports
10. Add pagination for large datasets
11. Add real-time notifications
12. Deploy with Docker and CI/CD
