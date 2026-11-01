# Deployment

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- MongoDB 7.0+

## Using Docker Compose
```bash
docker-compose up --build
```

Services:
- MongoDB on port 27017
- Backend API on port 8000

## Environment Variables
See `.env.example` for all configuration options.

## Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --port 8000
```

## Database Initialization
```bash
python scripts/initialize_database.py
python scripts/seed_skills.py
python scripts/create_admin.py
```

## Frontend Setup
```bash
cd frontend
python -m http.server 3000
# Or use any static file server
```

## Production Notes
- Change `SECRET_KEY` in `.env`
- Set `ENVIRONMENT=production`
- Use a proper WSGI server like Gunicorn
- Configure CORS origins properly
- Enable MongoDB authentication
- Set up SSL/TLS
