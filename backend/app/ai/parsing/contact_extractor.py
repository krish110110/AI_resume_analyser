import re
from typing import Optional

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(
    r"(?:(?<!\w)\+?\d{1,3}[\s.\-]?)?(?:\(?\d{2,4}\)?[\s.\-]?){1,4}\d{2,4}(?!\w)"
)

# Words that mark a heading rather than a person's name.
SECTION_KEYWORDS = {
    "resume", "curriculum", "vitae", "cv", "profile", "summary", "objective",
    "about", "contact", "experience", "education", "skills", "projects",
    "certifications", "certificates", "awards", "achievements", "interests",
    "hobbies", "references", "languages", "address", "email", "phone",
    "portfolio", "github", "linkedin", "work history", "employment",
    "professional", "career", "personal", "details", "information",
    "technical skills", "core competencies", "publications", "training",
}

NAME_STOPWORDS = {
    "engineer", "developer", "developer", "manager", "analyst", "scientist",
    "designer", "consultant", "architect", "specialist", "lead", "senior",
    "junior", "intern", "student", "graduate", "professor", "director",
}


class ContactExtractor:
    """Extracts the candidate name, email, and phone from resume text."""

    def extract(self, text: str) -> dict:
        """Return name, email, and phone found in the resume text."""
        if not text:
            return {"name": None, "email": None, "phone": None}

        lines = [line.strip() for line in text.splitlines()]

        email = self._find_email(text)
        phone = self._find_phone(text)
        name = self._find_name(lines)

        return {"name": name, "email": email, "phone": phone}

    def _find_email(self, text: str) -> Optional[str]:
        match = EMAIL_PATTERN.search(text)
        return match.group(0) if match else None

    def _find_phone(self, text: str) -> Optional[str]:
        """Find a phone number, skipping digits that belong to dates or metrics."""
        without_emails = EMAIL_PATTERN.sub(" ", text)

        candidates = []
        for line in without_emails.splitlines():
            # Skip date ranges such as "2019 - 2021" and "2020 - Present".
            if re.search(r"\b(19|20)\d{2}\b\s*[-–]\s*(\b(19|20)\d{2}\b|present)", line, re.IGNORECASE):
                continue
            candidates.append(line)

        for chunk in candidates:
            for match in PHONE_PATTERN.finditer(chunk):
                candidate = match.group(0).strip(" .,;|")
                digits = re.sub(r"\D", "", candidate)
                if 7 <= len(digits) <= 15:
                    return candidate
        return None

    def _find_name(self, lines: list) -> Optional[str]:
        """Find the candidate name, normally the first heading line."""
        for line in lines[:15]:
            candidate = self._clean_name_line(line)
            if candidate:
                return candidate
        return None

    def _clean_name_line(self, line: str) -> Optional[str]:
        if not line or len(line) > 60:
            return None

        lowered = line.lower()
        if "@" in line or any(keyword in lowered for keyword in SECTION_KEYWORDS):
            return None

        # A separator line such as "=====" or "-----" is not a name.
        if re.fullmatch(r"[\W_]+", line):
            return None

        # Strip common prefixes like "Name:" before validating.
        candidate = re.sub(r"^(name|candidate)\s*[:\-]\s*", "", line, flags=re.IGNORECASE).strip()
        if not candidate:
            return None

        words = candidate.split()
        if not 2 <= len(words) <= 4:
            return None

        # Every word must look like part of a name.
        for word in words:
            if not re.fullmatch(r"[A-Za-z][A-Za-z'\.\-]*", word):
                return None

        if any(word.lower() in NAME_STOPWORDS for word in words):
            return None

        return candidate