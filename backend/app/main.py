from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import connect_to_mongo, close_mongo_connection


app = FastAPI(
    title="AI Resume Analyzer API",
    description="AI-powered resume analysis and ATS scoring system",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    try:
        from app.models.interview_question import InterviewQuestion
        inserted = await InterviewQuestion.seed()
        if inserted:
            print(f"Seeded {inserted} interview questions")
    except Exception as e:
        print(f"Interview question seeding skipped: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-resume-analyzer"}
