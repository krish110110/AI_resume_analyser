from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.api.dependencies import get_current_active_user, require_admin
from app.services.dashboard_service import DashboardService
from app.services.resume_service import ResumeService
from app.repositories.resume_repository import ResumeRepository
from app.repositories.user_repository import UserRepository
from app.repositories.report_repository import ReportRepository
from app.core.constants import ResumeStatus, UserRole
from app.core.security import get_password_hash

router = APIRouter()


async def _user_display(user_id: str, field: str):
    if not user_id:
        return None
    user = await UserRepository.get_by_id(user_id)
    if not user:
        return None
    return getattr(user, field, None)


@router.get("/stats")
async def admin_stats(current_user: dict = Depends(require_admin)):
    return await DashboardService.get_admin_stats()


@router.post("/users")
async def create_user(
    payload: dict = Body(...),
    current_user: dict = Depends(require_admin),
):
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")
    role = payload.get("role", "user")

    if not email or not name or not password:
        raise HTTPException(status_code=400, detail="name, email and password are required")

    existing = await UserRepository.get_by_email(email)
    if existing:
        raise HTTPException(status_code=409, detail="User already exists with this email")

    try:
        role_enum = UserRole(role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = await UserRepository.create(
        name=name,
        email=email,
        hashed_password=get_password_hash(password),
        role=role_enum,
    )
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value, "is_active": user.is_active}


@router.get("/users")
async def list_users(search: str = "", current_user: dict = Depends(require_admin)):
    users = await UserRepository.list_all()
    if search:
        users = [u for u in users if search.lower() in u.name.lower() or search.lower() in u.email.lower()]
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role.value, "is_active": u.is_active} for u in users]


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(require_admin)):
    await UserRepository.delete(user_id)
    return {"message": "User deleted"}


@router.get("/users/{user_id}/analytics")
async def get_user_analytics(user_id: str, current_user: dict = Depends(require_admin)):
    user = await UserRepository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reports = await ReportRepository.list_by_user(user_id, limit=100)

    avg_ats = round(sum(r.ats_score for r in reports if r.ats_score is not None) / max(len([r for r in reports if r.ats_score is not None]), 1), 1) if reports else 0
    avg_similarity = round(sum(r.similarity_score for r in reports if r.similarity_score is not None) / max(len([r for r in reports if r.similarity_score is not None]), 1), 1) if reports else 0
    avg_skill_match = round(sum(r.skill_match_percentage for r in reports if r.skill_match_percentage is not None) / max(len([r for r in reports if r.skill_match_percentage is not None]), 1), 1) if reports else 0

    category_counts = {}
    for r in reports:
        cat = r.classification.get("category", "Unknown") if r.classification else "Unknown"
        category_counts[cat] = category_counts.get(cat, 0) + 1

    all_skills = []
    for r in reports:
        all_skills.extend(r.skills or [])

    skill_freq = {}
    for s in all_skills:
        skill_freq[s] = skill_freq.get(s, 0) + 1
    top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    reports_data = [
        {
            "id": r.id,
            "resume_id": r.resume_id,
            "filename": r.filename,
            "ats_score": r.ats_score,
            "similarity_score": r.similarity_score,
            "skill_match_percentage": r.skill_match_percentage,
            "skills": r.skills,
            "missing_keywords": r.missing_keywords,
            "recommendations": r.recommendations,
            "parsed_data": r.parsed_data,
            "features": r.features,
            "scores": r.scores,
            "classification": r.classification,
            "interview_questions": r.interview_questions,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in reports
    ]

    return {
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value, "is_active": user.is_active},
        "total_reports": len(reports),
        "avg_ats_score": avg_ats,
        "avg_similarity_score": avg_similarity,
        "avg_skill_match": avg_skill_match,
        "category_distribution": [{"category": k, "count": v} for k, v in category_counts.items()],
        "top_skills": [{"skill": k, "count": v} for k, v in top_skills],
        "reports": reports_data,
    }


@router.get("/reports")
async def list_reports(search: str = "", current_user: dict = Depends(require_admin)):
    reports = await ReportRepository.list_all()
    if search:
        reports = [r for r in reports if search.lower() in (r.filename or "").lower()]
    return [{
        "id": r.id,
        "resume_id": r.resume_id,
        "filename": r.filename,
        "ats_score": r.ats_score,
        "similarity_score": r.similarity_score,
        "skill_match_percentage": r.skill_match_percentage,
        "category": (r.classification or {}).get("category"),
        "level": (r.classification or {}).get("level"),
        "user_id": r.user_id,
        "user_name": await _user_display(r.user_id, "name"),
        "user_email": await _user_display(r.user_id, "email"),
        "created_at": r.created_at.isoformat() if r.created_at else None,
    } for r in reports]


@router.get("/reports/{report_id}")
async def get_report_detail(report_id: str, current_user: dict = Depends(require_admin)):
    report = await ReportRepository.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    resume = await ResumeRepository.get_by_id(report.resume_id) if report.resume_id else None
    resume_text = await ResumeService.get_resume_text(resume)

    return {
        "id": report.id,
        "resume_id": report.resume_id,
        "filename": report.filename,
        "user_id": report.user_id,
        "user_name": await _user_display(report.user_id, "name"),
        "user_email": await _user_display(report.user_id, "email"),
        "ats_score": report.ats_score,
        "similarity_score": report.similarity_score,
        "skill_match_percentage": report.skill_match_percentage,
        "skills": report.skills,
        "missing_keywords": report.missing_keywords,
        "recommendations": report.recommendations,
        "parsed_data": report.parsed_data,
        "features": report.features,
        "classification": report.classification,
        "scores": report.scores,
        "interview_questions": report.interview_questions,
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "resume": {
            "id": resume.id if resume else None,
            "filename": resume.filename if resume else report.filename,
            "file_type": resume.file_type if resume else None,
            "file_size": resume.file_size if resume else None,
            "status": resume.status.value if resume and isinstance(resume.status, ResumeStatus) else (resume.status if resume else None),
            "text": resume_text,
        } if resume or resume_text else None,
    }


@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(require_admin)):
    from collections import Counter

    users = await UserRepository.list_all()
    reports = await ReportRepository.list_all()

    user_months = {}
    report_months = {}
    ats_by_month = {}

    for u in users:
        month = u.created_at.strftime("%Y-%m") if u.created_at else "Unknown"
        user_months[month] = user_months.get(month, 0) + 1

    for r in reports:
        month = r.created_at.strftime("%Y-%m") if r.created_at else "Unknown"
        report_months[month] = report_months.get(month, 0) + 1
        if r.ats_score is not None:
            ats_by_month.setdefault(month, []).append(r.ats_score)

    all_months = sorted(set(list(user_months.keys()) + list(report_months.keys())))
    labels = all_months if all_months else ["No Data"]

    user_growth = [user_months.get(m, 0) for m in labels]
    report_volumes = [report_months.get(m, 0) for m in labels]
    ats_scores = [
        round(sum(ats_by_month.get(m, [0])) / max(len(ats_by_month.get(m, [1])), 1), 1)
        for m in labels
    ]

    skill_counter = Counter()
    for r in reports:
        for kw in r.missing_keywords or []:
            skill_counter[kw.lower()] += 1
    skill_gaps = [{"skill": k, "count": v} for k, v in skill_counter.most_common(10)]

    return {
        "labels": labels,
        "ats_scores": ats_scores,
        "report_volumes": report_volumes,
        "skill_gaps": skill_gaps,
        "user_growth": user_growth,
    }
