import os
import joblib
import numpy as np
import re
from typing import List


class QualityClassifier:
    def __init__(self):
        self.classifier = None
        self.regressor = None
        self.vectorizer = None
        self.label_encoder = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained quality classifier models."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        artifacts_dir = os.path.join(project_root, "ml", "artifacts", "quality_classifier")
        
        classifier_path = os.path.join(artifacts_dir, "classifier.pkl")
        regressor_path = os.path.join(artifacts_dir, "regressor.pkl")
        vectorizer_path = os.path.join(artifacts_dir, "vectorizer.pkl")
        encoder_path = os.path.join(artifacts_dir, "label_encoder.pkl")
        
        if all(os.path.exists(p) for p in [classifier_path, regressor_path, vectorizer_path, encoder_path]):
            self.classifier = joblib.load(classifier_path)
            self.regressor = joblib.load(regressor_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.label_encoder = joblib.load(encoder_path)
            print("Loaded quality classifier models")
        else:
            print("Quality classifier models not found, using fallback")
            self.label_encoder = None
    
    def _create_text_features(self, text: str) -> str:
        """Create text representation for quality prediction."""
        skill_keywords = [
            "python", "java", "javascript", "react", "node.js", "sql", "aws", "docker", "kubernetes",
            "machine learning", "data analysis", "project management", "agile", "scrum", "git",
            "typescript", "go", "rust", "c++", "c#", ".net", "php", "ruby", "swift", "kotlin",
            "tensorflow", "pytorch", "spark", "hadoop", "mongodb", "postgresql", "mysql",
            "redis", "elasticsearch", "graphql", "rest api", "microservices", "ci/cd", "terraform",
            "ansible", "jenkins", "linux", "bash", "powershell", "azure", "gcp", "tableau", "power bi"
        ]
        
        lower = text.lower()
        found_skills = [s for s in skill_keywords if s in lower]
        
        # Education
        edu = ""
        if any(kw in lower for kw in ['phd', 'doctorate']):
            edu = "phd"
        elif any(kw in lower for kw in ['master', 'mba', 'm.s.', 'ms ']):
            edu = "master"
        elif any(kw in lower for kw in ['bachelor', 'b.s.', 'bs ', 'degree']):
            edu = "bachelor"
        
        # Experience
        exp_match = re.search(r'(\d+)\s*(?:years?|yrs?)', lower)
        exp = f"experience years {exp_match.group(1)}" if exp_match else "experience years 0"
        
        return f"{' '.join(found_skills)} {edu} {exp}"
    
    async def predict_quality_score(self, text: str) -> float:
        if self.regressor is None:
            return round(self._heuristic_quality(text), 1)

        features_text = self._create_text_features(text)
        X = self.vectorizer.transform([features_text])
        score = self.regressor.predict(X)[0]
        return round(float(np.clip(score, 0, 100)), 1)

    def _heuristic_quality(self, text: str) -> float:
        """Deterministic quality score derived from resume content."""
        import re

        body = text or ""
        lower = body.lower()

        from app.core.skill_catalog import CANONICAL_SKILLS

        skill_count = sum(1 for s in CANONICAL_SKILLS if s.lower() in lower)
        years = [int(y) for y in re.findall(r"(\d+)\s*(?:years?|yrs?)", lower)]
        max_years = max(years) if years else 0
        has_email = "@" in body
        has_phone = bool(re.search(r"\(?\d{3,4}\)?[\s.\-]?\d{3,4}[\s.\-]?\d{4}", body))
        has_education = any(k in lower for k in ("bachelor", "master", "phd", "degree", "diploma", "b.tech", "m.tech"))
        has_experience = any(k in lower for k in ("experience", "employment", "internship", "work history"))
        has_projects = "project" in lower
        word_count = len(body.split())

        score = 20.0
        score += min(skill_count, 15) * 2.0
        score += min(max_years, 10) * 1.5
        score += 8 if has_education else 0
        score += 8 if has_experience else 0
        score += 5 if has_projects else 0
        score += 5 if has_email else 0
        score += 5 if has_phone else 0
        score += min(word_count / 500.0, 1.0) * 10
        return float(np.clip(score, 0, 100))

    async def predict_issues(self, text: str) -> List[str]:
        """Detect concrete resume issues from the actual content."""
        import re

        body = text or ""
        lower = body.lower()
        score = await self.predict_quality_score(text)

        from app.core.skill_catalog import CANONICAL_SKILLS

        issues = []

        skill_count = sum(1 for s in CANONICAL_SKILLS if s.lower() in lower)
        if skill_count < 5:
            issues.append("Skills section could be stronger")
        if not re.search(r"\d+%|\d+ (?:users|customers|requests|records|people)", lower):
            issues.append("Missing quantifiable achievements")
        if not any(k in lower for k in ("summary", "objective", "profile")):
            issues.append("Consider adding a professional summary")
        if "project" not in lower:
            issues.append("Add more specific project details")
        if not any(k in lower for k in ("certification", "certificate", "aws certified", "certified")):
            issues.append("Include relevant certifications")
        if not any(k in lower for k in ("lead", "led", "managed", "mentored", "owned")):
            issues.append("Include leadership experience")
        if len(body.split()) < 200:
            issues.append("Resume is quite short, add more detail")

        # Only report the most significant issues first.
        issues.sort(key=lambda issue: 0 if issue in (
            "Missing quantifiable achievements", "Skills section could be stronger"
        ) else 1)
        limit = 1 if score >= 85 else 3 if score >= 70 else 5
        return issues[:limit]


# Backward compatibility
async def predict_quality_score(text: str) -> float:
    classifier = QualityClassifier()
    return await classifier.predict_quality_score(text)

async def predict_issues(text: str) -> List[str]:
    classifier = QualityClassifier()
    return await classifier.predict_issues(text)