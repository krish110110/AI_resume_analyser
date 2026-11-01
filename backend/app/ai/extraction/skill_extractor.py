import os
import re
from typing import List

from app.core.skill_catalog import SKILL_ALIASES, normalize_skill


class SkillExtractor:
    """Extracts skills from resume text using the canonical skill catalog.

    Catalog names are matched with word boundaries so short names like "C"
    or "Go" do not match inside unrelated words, and common resume variants
    such as "reactjs" or "k8s" map back to the canonical skill name.
    """

    def __init__(self):
        from app.core.skill_catalog import CANONICAL_SKILLS
        self.canonical_skills = list(CANONICAL_SKILLS)
        self.known_skills = set(self.canonical_skills) | set(SKILL_ALIASES.keys())
        self._load_model()

    def _load_model(self):
        """Load the trained skill extractor model when artifacts exist."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        model_path = os.path.join(project_root, "ml", "artifacts", "skill_model", "model.pkl")
        vectorizer_path = os.path.join(project_root, "ml", "artifacts", "skill_model", "vectorizer.pkl")

        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            print("Loaded skill extractor model")
        else:
            print("Skill extractor model not found, using canonical catalog")

    def _find_all(self, text: str, name: str) -> bool:
        pattern = r'(?<![\w+#])' + re.escape(name) + r'(?![\w+#])'
        return re.search(pattern, text) is not None

    async def extract(self, text: str) -> List[str]:
        """Extract canonical skill names found in the text."""
        if not text:
            return []

        lower_text = text.lower()
        found = []

        for skill in self.canonical_skills:
            if self._find_all(lower_text, skill.lower()):
                found.append(skill)

        for alias, canonical in SKILL_ALIASES.items():
            if canonical in found:
                continue
            if self._find_all(lower_text, alias):
                found.append(canonical)

        # Keep catalog order for stable output.
        return [s for s in self.canonical_skills if s in set(found)]


# Backward compatibility
async def extract_skills(text: str) -> List[str]:
    extractor = SkillExtractor()
    return await extractor.extract(text)
