from typing import Dict, List, Optional
from app.ai.parsing.resume_parser import ResumeParser
from app.ai.parsing.text_cleaner import TextCleaner
from app.ai.parsing.section_detector import SectionDetector
from app.ai.parsing.contact_extractor import ContactExtractor
from app.ai.extraction.skill_extractor import SkillExtractor
from app.ai.extraction.education_extractor import EducationExtractor
from app.ai.extraction.experience_extractor import ExperienceExtractor
from app.ai.extraction.project_extractor import ProjectExtractor
from app.ai.extraction.certification_extractor import CertificationExtractor
from app.ai.classification.resume_classifier import ResumeClassifier
from app.ai.classification.quality_classifier import QualityClassifier
from app.ai.similarity.similarity_service import SimilarityService
from app.ai.scoring.ats_predictor import ATSPredictor
from app.ai.scoring.score_explainer import ScoreExplainer
from app.ai.skills.skill_matcher import SkillMatcher
from app.ai.skills.missing_skill_detector import MissingSkillDetector
from app.ai.recommendations.suggestion_generator import SuggestionGenerator
from app.ai.interview.question_retriever import QuestionRetriever


class AnalysisPipeline:
    """Main analysis pipeline that orchestrates the resume analysis workflow."""

    def __init__(self) -> None:
        """Initialize the analysis pipeline with all required components."""
        self.parser = ResumeParser()
        self.text_cleaner = TextCleaner()
        self.section_detector = SectionDetector()
        self.contact_extractor = ContactExtractor()
        self.skill_extractor = SkillExtractor()
        self.education_extractor = EducationExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.project_extractor = ProjectExtractor()
        self.certification_extractor = CertificationExtractor()
        self.resume_classifier = ResumeClassifier()
        self.quality_classifier = QualityClassifier()
        self.similarity_service = SimilarityService()
        self.ats_predictor = ATSPredictor()
        self.score_explainer = ScoreExplainer()
        self.skill_matcher = SkillMatcher()
        self.missing_skill_detector = MissingSkillDetector()
        self.suggestion_generator = SuggestionGenerator()
        self.question_retriever = QuestionRetriever()

    async def analyze(self, text: str, job_description: Optional[str] = None) -> Dict:
        parsed_data = await self._parse_resume(text)
        features = await self._extract_features(parsed_data)
        classification = await self._classify_resume(features)
        scores = await self._calculate_scores(features, job_description, classification)
        recommendations = await self._generate_recommendations(scores, features, classification, parsed_data)
        interview_questions = await self._generate_interview_questions(features)

        return {
            "parsed_data": parsed_data,
            "features": features,
            "classification": classification,
            "scores": scores,
            "recommendations": recommendations,
            "interview_questions": interview_questions,
        }

    async def _parse_resume(self, text: str) -> Dict:
        """Parse the raw resume text into structured sections.

        Args:
            text: The raw resume text.

        Returns:
            A dictionary containing parsed sections and metadata.
        """
        cleaned_text = self.text_cleaner.clean(text)
        sections = self.section_detector.detect_sections(cleaned_text)
        contact = self.contact_extractor.extract(cleaned_text)
        return {
            "cleaned_text": cleaned_text,
            "sections": sections,
            "raw_text": text,
            # Taken from the uploaded resume, never a fixed placeholder.
            "name": contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
        }

    async def _extract_features(self, parsed_data: Dict) -> Dict:
        """Extract features from the parsed resume data.

        Args:
            parsed_data: The parsed resume data dictionary.

        Returns:
            A dictionary containing extracted features.
        """
        text = parsed_data.get("cleaned_text", "")
        sections = parsed_data.get("sections", {})

        skills = await self.skill_extractor.extract(text)
        education = await self.education_extractor.extract(text)
        experience = await self.experience_extractor.extract(text)
        projects = await self.project_extractor.extract(text)
        certifications = await self.certification_extractor.extract(text)

        return {
            "cleaned_text": text,
            "skills": skills,
            "education": education,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "sections": sections,
        }

    async def _classify_resume(self, features: Dict) -> Dict:
        """Classify the resume into categories and quality levels.

        Args:
            features: The extracted features dictionary.

        Returns:
            A dictionary containing classification results.
        """
        text = features.get("cleaned_text", "")
        category = await self.resume_classifier.predict_category(text)
        level = await self.resume_classifier.predict_level(text)
        quality_score = await self.quality_classifier.predict_quality_score(text)
        issues = await self.quality_classifier.predict_issues(text)

        return {
            "category": category,
            "level": level,
            "quality_score": quality_score,
            "issues": issues,
        }

    async def _calculate_scores(self, features: Dict, job_description: Optional[str] = None, classification: Dict = None) -> Dict:
        """Calculate various scores for the resume.

        Args:
            features: The extracted features dictionary.
            job_description: Optional job description for similarity scoring.
            classification: Classification results (category, level).

        Returns:
            A dictionary containing calculated scores.
        """
        text = features.get("cleaned_text", "")
        skills = features.get("skills", [])

        ats_result = await self.ats_predictor.predict_score(text, job_description, features=features)
        ats_breakdown = await self.ats_predictor.get_score_breakdown(features, job_description)

        similarity = 0.0
        similarity_breakdown = {}
        missing_keywords = []

        if job_description:
            similarity = await self.similarity_service.calculate_similarity(text, job_description)
            similarity_breakdown = await self.similarity_service.get_similarity_breakdown(features, {})
            job_skills = await self.skill_extractor.extract(job_description)
            missing_keywords = await self.missing_skill_detector.detect(
                skills, job_skills,
                category=classification.get("category") if classification else None,
                level=classification.get("level") if classification else None,
                experience=features.get("experience", []),
            )
        else:
            missing_keywords = await self.missing_skill_detector.detect(
                skills, [],
                category=classification.get("category") if classification else None,
                level=classification.get("level") if classification else None,
                experience=features.get("experience", []),
            )

        match_percentage = 0.0
        if job_description:
            job_skills = await self.skill_extractor.extract(job_description)
            match_percentage = await self.skill_matcher.calculate_match_percentage(skills, job_skills)

        return {
            "ats_score": ats_result.get("score", 0.0),
            "ats_breakdown": ats_breakdown,
            "similarity_score": similarity,
            "similarity_breakdown": similarity_breakdown,
            "skill_match_percentage": match_percentage,
            "missing_keywords": missing_keywords,
        }

    async def _generate_interview_questions(self, features: Dict) -> List[dict]:
        """Fetch database-backed interview questions for the extracted skills.

        Args:
            features: The extracted features dictionary.

        Returns:
            A list of skill groups, each with skill, category, and questions.
        """
        skills = features.get("skills", [])
        if not skills:
            return []
        try:
            return await self.question_retriever.retrieve(skills)
        except Exception:
            return []

    async def _generate_recommendations(self, scores: Dict, features: Dict, classification: Dict = None, parsed_data: Dict = None) -> List[str]:
        """Generate recommendations based on scores and features.

        Args:
            scores: The calculated scores dictionary.
            features: The extracted features dictionary.
            classification: Classification results (category, level).
            parsed_data: Parsed resume data, used to address the candidate by name.

        Returns:
            A list of recommendation strings.
        """
        candidate_name = (parsed_data or {}).get("name") or ""
        feedback = await self.score_explainer.generate_feedback(scores, candidate_name)

        missing_keywords = scores.get("missing_keywords", [])
        recommendations = list(feedback)
        address = f"{candidate_name}, " if candidate_name else ""

        if missing_keywords:
            if len(missing_keywords) <= 3:
                recommendations.append(f"{address}consider adding these missing skills: {', '.join(missing_keywords)}")
            else:
                recommendations.append(
                    f"{address}your resume is missing {len(missing_keywords)} recommended skills. "
                    f"Key ones to add: {', '.join(missing_keywords[:5])}"
                )

        return recommendations
