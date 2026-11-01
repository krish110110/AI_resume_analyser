import os
import joblib
import numpy as np
from typing import List, Optional


class ResumeClassifier:
    def __init__(self):
        self.category_model = None
        self.level_model = None
        self.vectorizer = None
        self.cat_encoder = None
        self.level_encoder = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained classifier models."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        artifacts_dir = os.path.join(project_root, "ml", "artifacts", "classifier")
        
        cat_model_path = os.path.join(artifacts_dir, "category_model.pkl")
        level_model_path = os.path.join(artifacts_dir, "level_model.pkl")
        vectorizer_path = os.path.join(artifacts_dir, "vectorizer.pkl")
        cat_encoder_path = os.path.join(artifacts_dir, "cat_encoder.pkl")
        level_encoder_path = os.path.join(artifacts_dir, "level_encoder.pkl")
        
        if all(os.path.exists(p) for p in [cat_model_path, level_model_path, vectorizer_path, cat_encoder_path, level_encoder_path]):
            self.category_model = joblib.load(cat_model_path)
            self.level_model = joblib.load(level_model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.cat_encoder = joblib.load(cat_encoder_path)
            self.level_encoder = joblib.load(level_encoder_path)
            print("Loaded resume classifier models")
        else:
            print("Classifier models not found, using fallback")
            self.cat_encoder = None
            self.level_encoder = None
    
    def _create_text_features(self, text: str) -> str:
        """Create text representation for classification."""
        from app.core.skill_catalog import CANONICAL_SKILLS

        lower = text.lower()
        found_skills = [s for s in CANONICAL_SKILLS if s.lower() in lower]

        # Education
        edu = ""
        if any(kw in lower for kw in ['phd', 'doctorate']):
            edu = "phd"
        elif any(kw in lower for kw in ['master', 'mba', 'm.s.', 'ms ']):
            edu = "master"
        elif any(kw in lower for kw in ['bachelor', 'b.s.', 'bs ', 'degree']):
            edu = "bachelor"

        # Experience
        import re
        exp_match = re.search(r'(\d+)\s*(?:years?|yrs?)', lower)
        exp = f"experience years {exp_match.group(1)}" if exp_match else "experience years 0"

        return f"{' '.join(found_skills)} {edu} {exp}"

    CATEGORY_KEYWORDS = {
        "Data Science": ["machine learning", "pandas", "numpy", "scikit-learn", "tensorflow",
                         "pytorch", "data analysis", "statistics", "matplotlib", "seaborn", "r "],
        "Data Engineering": ["airflow", "apache spark", "kafka", "hadoop", "pyspark", "data pipeline",
                             "etl", "data warehouse"],
        "DevOps": ["kubernetes", "docker", "terraform", "ansible", "jenkins", "ci/cd", "aws",
                   "prometheus", "grafana", "infrastructure"],
        "Mobile Development": ["android", "ios", "swift", "kotlin", "flutter", "react native", "dart"],
        "Frontend Engineering": ["react.js", "angular", "vue.js", "html", "css", "frontend", "tailwind"],
        "Data Engineering": ["airflow", "apache spark", "kafka", "hadoop", "pyspark", "etl", "data warehouse"],
    }

    LEVEL_KEYWORDS = {
        "Lead": ["lead", "head of", "director", "principal", "manager", "architect"],
        "Senior": ["senior", "sr.", "staff", "8 years", "10 years", "expert"],
        "Mid": ["mid", "intermediate", "3 years", "4 years", "5 years", "6 years"],
        "Junior": ["junior", "jr.", "entry", "fresher", "trainee", "intern", "0 years", "1 year"],
    }

    def _keyword_fallback_category(self, text: str) -> str:
        """Derive the category from skills mentioned in the resume."""
        lower = (text or "").lower()
        scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            scores[category] = sum(1 for kw in keywords if kw in lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "Software Engineering"

    def _keyword_fallback_level(self, text: str) -> str:
        """Derive the seniority level from titles and years of experience."""
        import re

        lower = (text or "").lower()
        years = [int(y) for y in re.findall(r"(\d+)\s*(?:years?|yrs?)", lower)]
        max_years = max(years) if years else 0

        if max_years >= 10:
            return "Lead"
        if max_years >= 6:
            return "Senior"
        if max_years >= 3:
            return "Mid"
        if max_years >= 1:
            return "Junior"

        for level in ("Lead", "Senior", "Mid", "Junior"):
            if any(kw in lower for kw in self.LEVEL_KEYWORDS[level]):
                return level
        return "Junior"

    async def predict_category(self, text: str) -> str:
        if self.category_model is None:
            return self._keyword_fallback_category(text)

        features_text = self._create_text_features(text)
        X = self.vectorizer.transform([features_text])
        pred = self.category_model.predict(X)[0]
        return self.cat_encoder.inverse_transform([pred])[0]

    async def predict_level(self, text: str) -> str:
        """Predict seniority, trusting explicit years of experience when present.

        Years are a direct signal for seniority, so they take precedence over the
        model whenever the resume states them.
        """
        years_level = self._level_from_years(text)
        if years_level:
            return years_level

        if self.level_model is None:
            return self._keyword_fallback_level(text)

        features_text = self._create_text_features(text)
        X = self.vectorizer.transform([features_text])
        pred = self.level_model.predict(X)[0]
        return self.level_encoder.inverse_transform([pred])[0]

    def _level_from_years(self, text: str) -> Optional[str]:
        """Map stated years of experience onto a seniority level."""
        import re

        lower = (text or "").lower()
        years = [int(y) for y in re.findall(r"(\d+)\s*(?:\+)?\s*(?:years?|yrs?)", lower)]
        if not years:
            return None

        max_years = max(years)
        if max_years >= 10:
            return "Lead"
        if max_years >= 6:
            return "Senior"
        if max_years >= 3:
            return "Mid"
        if max_years >= 1:
            return "Junior"
        return "Junior"


# Backward compatibility
async def predict_category(text: str) -> str:
    classifier = ResumeClassifier()
    return await classifier.predict_category(text)

async def predict_level(text: str) -> str:
    classifier = ResumeClassifier()
    return await classifier.predict_level(text)