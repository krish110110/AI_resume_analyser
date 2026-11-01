import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection
from app.models.report import Report

async def main():
    await connect_to_mongo()
    reports = await Report.list_by_user("all")
    print("Total reports:", len(reports))
    for r in reports[:10]:
        print("REPORT:", r.id, "|", r.filename, "|", r.user_id, "|", r.resume_id, "|", r.ats_score)
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
