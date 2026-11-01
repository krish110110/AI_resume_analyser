from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserRegister, UserLogin, Token, PasswordResetRequest, PasswordReset
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(payload: UserRegister):
    try:
        user = await AuthService.register(payload.name, payload.email, payload.password)
        access = AuthService.create_access_token(user.id, user.role)
        refresh = AuthService.create_refresh_token(user.id, user.role)
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value}}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=dict)
async def login(payload: UserLogin):
    user = await AuthService.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access = AuthService.create_access_token(user.id, user.role)
    refresh = AuthService.create_refresh_token(user.id, user.role)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value}}


@router.post("/refresh", response_model=Token)
async def refresh(payload: dict):
    token = payload.get("refresh_token")
    from app.core.security import decode_token
    data = decode_token(token)
    if not data or data.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    from app.repositories.user_repository import UserRepository
    user = await UserRepository.get_by_id(data.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    access = AuthService.create_access_token(user.id, user.role)
    refresh = AuthService.create_refresh_token(user.id, user.role)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(payload: PasswordResetRequest):
    return {"message": "If an account exists, a reset link has been sent."}
