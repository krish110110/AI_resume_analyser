from fastapi import APIRouter, Depends, HTTPException, Body
from app.api.dependencies import get_current_active_user, require_admin
from app.models.interview_question import InterviewQuestion
from app.services.interview_service import InterviewService

router = APIRouter()


@router.get("/")
async def list_questions(current_user: dict = Depends(require_admin)):
    """Return the full interview question bank (admin only)."""
    questions = await InterviewQuestion.list_all()
    return {
        "total": len(questions),
        "questions": questions,
    }


@router.get("/stats")
async def question_stats(current_user: dict = Depends(require_admin)):
    return await InterviewQuestion.stats()


@router.get("/skills")
async def list_skills(current_user: dict = Depends(require_admin)):
    return {"skills": await InterviewQuestion.skills_covered()}


@router.get("/by-skill/{skill}")
async def questions_by_skill(skill: str, current_user: dict = Depends(require_admin)):
    questions = await InterviewQuestion.list_by_skill(skill)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for that skill")
    return {"skill": skill, "total": len(questions), "questions": questions}


@router.get("/by-resume/{resume_id}")
async def questions_by_resume(resume_id: str, current_user: dict = Depends(get_current_active_user)):
    """Return interview questions matched to the skills in an analyzed resume."""
    result = await InterviewService.generate_for_resume(resume_id)
    if not result["questions"]:
        raise HTTPException(status_code=404, detail="No interview questions available for this resume")
    return result


@router.post("/generate")
async def generate_questions(
    payload: dict = Body(...),
    current_user: dict = Depends(get_current_active_user),
):
    """Generate interview questions for an explicit list of skills."""
    skills = payload.get("skills") or []
    per_skill = int(payload.get("per_skill") or 2)
    if not skills:
        raise HTTPException(status_code=400, detail="skills is required")
    return await InterviewService.get_for_skills(skills, per_skill=per_skill)


@router.post("/seed")
async def seed_questions(
    payload: dict = Body(default={}),
    current_user: dict = Depends(require_admin),
):
    """Seed the question bank into the database (admin only)."""
    force = bool(payload.get("force"))
    inserted = await InterviewQuestion.seed(force=force)
    return {
        "inserted": inserted,
        "stats": await InterviewQuestion.stats(),
    }
