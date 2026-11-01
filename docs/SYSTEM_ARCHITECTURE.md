# System Architecture

## Overview
AI Resume Analyzer is a full-stack application with FastAPI backend, MongoDB database, and vanilla JS frontend.

## Backend Architecture
- **FastAPI**: Async web framework
- **Motor**: Async MongoDB driver
- **Pydantic v2**: Data validation
- **JWT**: Authentication

### Layers
1. **API Layer**: `app/api/v1/` - Route handlers
2. **Service Layer**: `app/services/` - Business logic
3. **Repository Layer**: `app/repositories/` - Data access
4. **Model Layer**: `app/models/` - MongoDB documents
5. **Schema Layer**: `app/schemas/` - Pydantic models
6. **AI Layer**: `app/ai/` - ML pipeline

## Frontend Architecture
- **Vanilla JS**: No framework dependencies
- **Chart.js**: Data visualization
- **Fetch API**: HTTP client

## ML Pipeline
- **Parsing**: Text cleaning and section detection
- **Extraction**: Skills, education, experience, projects, certifications
- **Classification**: Resume category and quality
- **Scoring**: ATS prediction and explanation
- **Similarity**: Sentence embeddings and FAISS
- **Recommendations**: Skill gap analysis and suggestions

## Data Flow
1. User uploads resume
2. File saved to storage
3. Text extracted from PDF/DOCX
4. AI pipeline analyzes text
5. Scores and recommendations generated
6. Report stored in MongoDB
7. Frontend displays results
