import os
import uuid
from datetime import datetime
from typing import Optional
from app.core.config import settings
from app.core.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from app.repositories.resume_repository import ResumeRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.ai.pipeline.analysis_pipeline import AnalysisPipeline


class ResumeService:
    @staticmethod
    def validate_file(file):
        ext = file.filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}")
        size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)
        if size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"File too large. Max {MAX_FILE_SIZE_MB}MB")
        return ext

    @staticmethod
    async def create_resume(user_id: str, filename: str, file_path: str, file_type: str, file_size: int):
        return await ResumeRepository.create(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            status="processing",
        )

    @staticmethod
    def extract_text(file_path: str) -> str:
        if not file_path or not os.path.exists(file_path):
            return ""
        lower = file_path.lower()
        if lower.endswith('.pdf'):
            from app.utils.pdf_extractor import PdfExtractor
            return PdfExtractor.extract(file_path)
        if lower.endswith('.docx'):
            from app.utils.docx_extractor import DocxExtractor
            return DocxExtractor.extract(file_path)
        if lower.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                return f.read()
        return ""

    @staticmethod
    async def get_resume_text(resume) -> str:
        if not resume:
            return ""
        return getattr(resume, "raw_text", "") or ResumeService.extract_text(resume.file_path)

    @staticmethod
    async def process_resume(resume_id: str, job_description: Optional[str] = None):
        from app.models.resume import Resume
        resume = await Resume.get_by_id(resume_id)
        if not resume:
            raise ValueError("Resume not found")
        try:
            text = ResumeService.extract_text(resume.file_path)
            pipeline = AnalysisPipeline()
            result = await pipeline.analyze(text, job_description)
            resume.status = "completed"
            resume.ats_score = result.get("scores", {}).get("ats_score", 0.0)
            resume.similarity_score = result.get("scores", {}).get("similarity_score")
            resume.skill_match_percentage = result.get("scores", {}).get("skill_match_percentage")
            resume.missing_keywords = result.get("scores", {}).get("missing_keywords", [])
            resume.raw_text = text
            await resume.save()
            analysis = await AnalysisRepository.create(
                resume_id=resume_id,
                job_description_id=None,
                parsed_data=result.get("parsed_data", {}),
                features=result.get("features", {}),
                classification=result.get("classification", {}),
                scores=result.get("scores", {}),
                recommendations=result.get("recommendations", []),
                interview_questions=result.get("interview_questions", []),
            )
            report = await ReportRepository.create(
                user_id=resume.user_id,
                resume_id=resume_id,
                analysis_id=analysis.id,
                filename=resume.filename,
                ats_score=resume.ats_score,
                similarity_score=resume.similarity_score,
                skill_match_percentage=resume.skill_match_percentage,
                skills=result.get("features", {}).get("skills", []),
                missing_keywords=resume.missing_keywords,
                recommendations=result.get("recommendations", []),
                parsed_data=result.get("parsed_data", {}),
                features=result.get("features", {}),
                classification=result.get("classification", {}),
                scores=result.get("scores", {}),
                interview_questions=result.get("interview_questions", []),
            )
            return resume, analysis, report
        except Exception as e:
            resume.status = "failed"
            await resume.save()
            raise e

    @staticmethod
    async def list_resumes(user_id: str, limit: int = 50):
        return await ResumeRepository.list_by_user(user_id, limit)

    @staticmethod
    async def get_resume(resume_id: str):
        return await ResumeRepository.get_by_id(resume_id)

    @staticmethod
    async def delete_resume(resume_id: str):
        await ResumeRepository.delete(resume_id)
