from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_active_user
from app.services.user_service import UserService
from app.schemas.user import UserUpdate

router = APIRouter()


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_active_user)):
    user = await UserService.get_profile(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value}


@router.put("/me")
async def update_me(payload: UserUpdate, current_user: dict = Depends(get_current_active_user)):
    user = await UserService.update_profile(current_user["user_id"], payload)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value}
