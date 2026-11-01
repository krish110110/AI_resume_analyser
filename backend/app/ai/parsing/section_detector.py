import re


class SectionDetector:
    def detect_sections(self, text: str) -> dict:
        sections = {}
        # More flexible patterns that work with various formatting
        patterns = {
            "skills": r'(?i)(?:skills?|technical skills?|core competencies)\s*[:\-]?\s*(.*?)(?:\n\s*(?:experience|education|projects?|certifications?)\b|\Z)',
            "experience": r'(?i)(?:experience|work experience|employment history)\s*[:\-]?\s*(.*?)(?:\n\s*(?:education|skills?|projects?|certifications?)\b|\Z)',
            "education": r'(?i)(?:education|academic background|qualifications)\s*[:\-]?\s*(.*?)(?:\n\s*(?:experience|skills?|projects?|certifications?)\b|\Z)',
            "projects": r'(?i)(?:projects?|personal projects?)\s*[:\-]?\s*(.*?)(?:\n\s*(?:experience|education|skills?|certifications?)\b|\Z)',
            "certifications": r'(?i)(?:certifications?|licenses?|credentials)\s*[:\-]?\s*(.*?)(?:\n\s*(?:experience|education|skills?|projects?)\b|\Z)',
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = match.group(1).strip()
            else:
                sections[key] = ""
        return sections
