from pydantic import BaseModel


class UserDashboardStats(BaseModel):
    total_resumes: int
    avg_ats_score: float
    total_matches: int


class AdminDashboardStats(BaseModel):
    total_users: int
    total_resumes: int
    avg_ats_score: float
    system_health: str
