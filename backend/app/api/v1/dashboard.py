from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_active_user, require_admin
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/user")
async def user_dashboard(current_user: dict = Depends(get_current_active_user)):
    return await DashboardService.get_user_stats(current_user["user_id"])


@router.get("/admin")
async def admin_dashboard(current_user: dict = Depends(require_admin)):
    return await DashboardService.get_admin_stats()
