import re


class ProjectExtractor:
    async def extract(self, text: str) -> list[dict]:
        matches = re.findall(r'(?i)project[:\-]?\s*(.*?)(?:\n|$)', text)
        return [{"name": m.strip()} for m in matches[:10]]
