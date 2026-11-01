import os
import re
from typing import Dict, Optional


class ATSPredictor:
    """Predict ATS compatibility score from extracted resume features."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self._load_model()

    def _load_model(self):
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        model_path = os.path.join(project_root, "ml", "artifacts", "ats_predictor", "model.pkl")
        scaler_path = os.path.join(project_root, "ml", "artifacts", "ats_predictor", "scaler.pkl")
        features_path = os.path.join(project_root, "ml", "artifacts", "ats_predictor", "feature_names.pkl")

        if os.path.exists(model_path):
            import joblib
            self.model = joblib.load(model_path)
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            if os.path.exists(features_path):
                self.feature_names = joblib.load(features_path)
            print("Loaded ATS predictor model")
        else:
            print("ATS predictor model not found, using feature-based fallback")

    async def predict_score(self, text: str, job_description: Optional[str], features: Optional[Dict] = None) -> dict:
        if features:
            score = self._feature_based_score(features, job_description)
        elif self.model is not None:
            score = self._ml_score(text, job_description)
        else:
            score = self._text_based_score(text, job_description)
        score = round(float(min(max(score, 15.0), 98.0)), 1)
        return {"score": score, "verdict": "Good" if score >= 70 else "Needs Improvement"}

    async def get_score_breakdown(self, features: Dict, job_description: Optional[str] = None) -> dict:
        if not features:
            return {}
        return self._compute_feature_breakdown(features, job_description)

    def _feature_based_score(self, features: Dict, job_description: Optional[str]) -> float:
        breakdown = self._compute_feature_breakdown(features, job_description)
        score = (
            breakdown["skills"] * 0.30
            + breakdown["experience"] * 0.25
            + breakdown["education"] * 0.20
            + breakdown["structure"] * 0.25
        )
        score += breakdown.get("job_bonus", 0.0)
        return min(max(score, 15.0), 98.0)

    def _compute_feature_breakdown(self, features: Dict, job_description: Optional[str]) -> dict:
        skills = features.get("skills", []) or []
        experience = features.get("experience", []) or []
        education = features.get("education", []) or []
        sections = features.get("sections", {}) or {}
        text = features.get("cleaned_text", "") or ""

        skills_score = self._score_skills(skills)
        exp_score = self._score_experience(experience, text)
        edu_score = self._score_education(education)
        struct_score = self._score_structure(skills, experience, education, sections, text)

        bonus = 0.0
        if job_description:
            bonus = self._score_job_match(skills, job_description)

        return {
            "skills": round(min(skills_score, 100.0), 2),
            "experience": round(min(exp_score, 100.0), 2),
            "education": round(min(edu_score, 100.0), 2),
            "structure": round(min(struct_score, 100.0), 2),
            "job_bonus": round(min(bonus, 10.0), 2),
        }

    def _score_skills(self, skills) -> float:
        if not skills:
            return 12.0
        core_technical = {
            "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Rust",
            "SQL", "React.js", "Node.js", "Docker", "Kubernetes", "AWS", "Machine Learning",
            "TensorFlow", "PyTorch", "PostgreSQL", "MongoDB", "Redis", "GraphQL",
            "Microservices", "Terraform", "Apache Spark", "Apache Kafka",
            "FastAPI", "Django", "Flask", "Spring Boot", ".NET", "HTML", "CSS",
            "Angular", "Vue.js", "Svelte", "Next.js", "Tailwind CSS", "Bootstrap",
            "Linux", "Bash", "Git", "GitHub", "GitHub Actions", "Jenkins",
            "Google Cloud Platform", "Microsoft Azure", "Elasticsearch", "Redis",
            "NumPy", "Pandas", "Matplotlib", "Seaborn", "Plotly",
            "Scikit-learn", "Keras", "XGBoost", "LightGBM", "CatBoost",
            "Hugging Face Transformers", "spaCy", "NLTK", "OpenCV", "FAISS",
            "Sentence Transformers", "LangChain", "LlamaIndex",
            "Airflow", "Selenium", "BeautifulSoup", "R", "Scala", "MATLAB",
        }
        total_count = len(skills)
        core_count = sum(1 for s in skills if s in core_technical)
        count_score = min(total_count / 15.0, 1.0) * 60.0
        tech_score = min(core_count / 8.0, 1.0) * 40.0
        return count_score + tech_score

    def _score_experience(self, experience, text: str) -> float:
        years = 0.0
        if experience:
            year_matches = []
            for exp in experience:
                if isinstance(exp, dict):
                    text_blob = " ".join(str(v) for v in exp.values())
                else:
                    text_blob = str(exp)
                m = re.search(r"(\d+)\s*(?:years?|yrs?)", text_blob.lower())
                if m:
                    year_matches.append(int(m.group(1)))
            if year_matches:
                years = max(year_matches)
        if years == 0:
            m = re.search(r"(\d+)\s*(?:years?|yrs?)", (text or "").lower())
            years = int(m.group(1)) if m else 0.0

        years_score = min(years / 10.0, 1.0) * 70.0

        has_experience = any(k in (text or "").lower() for k in ("experience", "employment", "work history", "internship"))
        section_score = 30.0 if has_experience else 8.0

        seniority_bonus = 0.0
        if years >= 10:
            seniority_bonus = 15.0
        elif years >= 7:
            seniority_bonus = 10.0
        elif years >= 4:
            seniority_bonus = 5.0
        elif years >= 2:
            seniority_bonus = 2.0

        return min(years_score + section_score + seniority_bonus, 100.0)

    def _score_education(self, education) -> float:
        if not education:
            return 18.0
        text = " ".join(str(e) for e in education).lower()
        if any(k in text for k in ("phd", "doctorate")):
            return 95.0
        if any(k in text for k in ("master", "mba", "m.tech", "msc", "m.s.", "m.sc")):
            return 82.0
        if any(k in text for k in ("bachelor", "b.tech", "bsc", "b.s.", "degree", "diploma")):
            return 65.0
        if any(k in text for k in ("certificate", "certification", "associate")):
            return 45.0
        return 25.0

    def _score_structure(self, skills, experience, education, sections, text: str) -> float:
        import re
        has_email = bool(re.search(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}", text or ""))
        has_phone = bool(re.search(r"\(?\d{3,4}\)?[\s.\-]?\d{3,4}[\s.\-]?\d{4}", text or ""))
        contact_score = (25.0 if has_email else 0.0) + (15.0 if has_phone else 0.0)

        section_keys = ("skills", "experience", "education", "projects", "certifications")
        section_count = sum(1 for k in section_keys if k in (text or "").lower())
        section_score = min(section_count / 4.0, 1.0) * 30.0

        length = len(text or "")
        if 900 <= length <= 4000:
            length_score = 20.0
        elif 500 <= length < 900:
            length_score = 12.0
        elif length > 4000:
            length_score = 10.0
        else:
            length_score = 4.0

        completeness = 0.0
        if skills:
            completeness += 5.0
        if experience:
            completeness += 3.0
        if education:
            completeness += 2.0

        return min(contact_score + section_score + length_score + completeness, 100.0)

    def _score_job_match(self, skills, job_description: str) -> float:
        if not skills or not job_description:
            return 0.0
        lower_job = job_description.lower()
        matched = sum(1 for s in skills if s.lower() in lower_job)
        if not matched:
            return 0.0
        return min((matched / max(len(skills), 1)) * 10.0, 10.0)

    def _text_based_score(self, text: str, job_description: Optional[str]) -> float:
        breakdown = self._compute_text_breakdown(text)
        score = (
            breakdown["keywords"] * 0.30
            + breakdown["experience"] * 0.25
            + breakdown["education"] * 0.20
            + breakdown["formatting"] * 0.25
        )
        if job_description:
            score = min(score + 5, 95)
        return score

    def _compute_text_breakdown(self, text: str) -> dict:
        lower = (text or "").lower()

        skill_keywords = [
            "python", "java", "javascript", "react.js", "node.js", "sql", "aws", "docker",
            "kubernetes", "machine learning", "pandas", "git", "typescript", "go", "rust",
            "c++", "c#", ".net", "php", "ruby", "swift", "kotlin", "tensorflow", "pytorch",
            "postgresql", "mongodb", "redis", "graphql", "rest api", "microservices",
            "terraform", "jenkins", "linux", "bash", "spark", "kafka", "airflow",
        ]
        found_skills = [s for s in skill_keywords if s in lower]
        keywords = min(len(found_skills) / 12.0, 1.0) * 30.0

        years_match = re.search(r"(\d+)\s*(?:years?|yrs?)", lower)
        years = int(years_match.group(1)) if years_match else 0
        has_experience = any(k in lower for k in ("experience", "employment", "work history", "internship"))
        experience = min(years / 8.0, 0.8) * 25.0 + (10.0 if has_experience else 3.0)
        if years >= 7:
            experience += 5.0
        elif years >= 4:
            experience += 3.0
        experience = min(experience, 25.0)

        if any(k in lower for k in ("phd", "doctorate")):
            education = 20.0
        elif any(k in lower for k in ("master", "mba", "m.tech", "msc", "m.s.")):
            education = 17.0
        elif any(k in lower for k in ("bachelor", "b.tech", "bsc", "b.s.", "degree", "diploma")):
            education = 14.0
        else:
            education = 6.0

        import re as _re
        has_email = bool(_re.search(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}", lower))
        has_phone = bool(_re.search(r"\(?\d{3,4}\)?[\s.\-]?\d{3,4}[\s.\-]?\d{4}", text or ""))
        sections = sum(1 for k in ("skills", "experience", "education", "projects", "certifications") if k in lower)
        length = len(text or "")
        if 800 <= length <= 3500:
            length_score = 5.0
        elif 400 <= length < 800:
            length_score = 3.0
        elif length > 3500:
            length_score = 3.5
        else:
            length_score = 1.5
        formatting = (4.0 if has_email else 0.0) + (3.0 if has_phone else 0.0) + min(sections / 4.0, 1.0) * 10.0 + length_score

        return {
            "keywords": round(keywords, 2),
            "experience": round(experience, 2),
            "education": round(education, 2),
            "formatting": round(min(formatting, 25.0), 2),
        }

    def _ml_score(self, text: str, job_description: Optional[str]) -> float:
        import numpy as np
        features = self._create_ml_features(text, job_description)
        if self.scaler:
            features = self.scaler.transform(features)
        raw = self.model.predict(features)[0]
        return float(min(max(raw, 15.0), 98.0))

    def _create_ml_features(self, text: str, job_description: Optional[str]) -> "np.ndarray":
        import numpy as np
        lower_text = text.lower()
        skill_keywords = [
            "python", "java", "javascript", "react.js", "node.js", "sql", "aws", "docker", "kubernetes",
            "machine learning", "pandas", "project management", "agile", "scrum", "git",
            "typescript", "go", "rust", "c++", "c#", ".net", "php", "ruby", "swift", "kotlin",
            "tensorflow", "pytorch", "spark", "hadoop", "mongodb", "postgresql", "mysql",
            "redis", "elasticsearch", "graphql", "rest api", "microservices", "terraform",
            "ansible", "jenkins", "linux", "bash", "microsoft azure", "google cloud platform",
            "tableau", "power bi",
        ]
        resume_skills = {s for s in skill_keywords if s in lower_text}
        if job_description:
            job_skills = {s for s in skill_keywords if s in job_description.lower()}
            skill_match = len(resume_skills & job_skills) / max(len(job_skills), 1)
            overlap_count = min(len(resume_skills & job_skills) / 10.0, 1.0)
        else:
            skill_match = min(len(resume_skills) / 10.0, 1.0)
            overlap_count = min(len(resume_skills) / 10.0, 1.0)

        exp_match = re.search(r'(\d+)\s*(?:years?|yrs?)', lower_text)
        exp_years = min(int(exp_match.group(1)) / 10.0, 1.0) if exp_match else 0.1

        if any(k in lower_text for k in ['phd', 'doctorate']):
            edu_level = 3
        elif any(k in lower_text for k in ['master', 'mba', 'm.s.', 'ms ']):
            edu_level = 2
        elif any(k in lower_text for k in ['bachelor', 'b.s.', 'bs ', 'degree']):
            edu_level = 1
        else:
            edu_level = 0

        num_skills = min(len(resume_skills) / 15.0, 1.0)
        return np.array([[skill_match, exp_years, edu_level, num_skills, overlap_count, num_skills]])


# Backward compatibility
async def predict_score(text: str, job_desc: Optional[str], features: Optional[Dict] = None) -> dict:
    predictor = ATSPredictor()
    return await predictor.predict_score(text, job_desc, features=features)
