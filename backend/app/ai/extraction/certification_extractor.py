import re


class CertificationExtractor:
    async def extract(self, text: str) -> list[dict]:
        matches = re.findall(r'(?i)certifications?[:\-]?\s*(.*?)(?:\n|$)', text)
        return [{"name": m.strip()} for m in matches[:10]]
