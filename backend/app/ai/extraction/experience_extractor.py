import re


class ExperienceExtractor:
    async def extract(self, text: str) -> list[dict]:
        lines = text.splitlines()
        experiences = []
        for line in lines:
            if re.search(r'\b(20\d{2}|19\d{2})\b', line):
                experiences.append({"raw": line.strip()})
        return experiences[:10]
