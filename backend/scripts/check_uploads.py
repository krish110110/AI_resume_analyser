import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection
from app.models.resume import Resume
from app.models.report import Report

async def main():
    await connect_to_mongo()
    resumes = await Resume.list_by_user("all")
    print("Total resumes:", len(resumes))
    for r in resumes[:5]:
        print("RESUME:", r.id, "|", r.filename, "|", r.status, "|", r.ats_score)
    
    reports = await Report.list_by_user("all")
    print("Total reports:", len(reports))
    for r in reports[:5]:
        print("REPORT:", r.id, "|", r.filename, "|", r.resume_id)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
