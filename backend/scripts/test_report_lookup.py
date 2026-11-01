import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database
from app.repositories.report_repository import ReportRepository

async def main():
    await connect_to_mongo()
    r = await ReportRepository.get_by_resume_id('6a81aebd5a245f16f717ba8d')
    print('Report:', r.id if r else None)
    if r:
        print('User ID:', r.user_id)
        print('Filename:', r.filename)
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
