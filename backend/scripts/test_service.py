import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.report_service import ReportService

async def main():
    await connect_to_mongo()
    r = await ReportService.get_report("6a81aec15a245f16f717ba8f")
    print("Report:", r.id if r else None)
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
