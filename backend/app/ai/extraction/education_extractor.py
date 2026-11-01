import re


class EducationExtractor:
    async def extract(self, text: str) -> list[dict]:
        degrees = ["bachelor", "master", "phd", "doctorate", "mba", "b.tech", "m.tech", "bsc", "msc"]
        found = []
        for line in text.splitlines():
            for deg in degrees:
                if deg in line.lower():
                    found.append({"degree": deg, "raw": line.strip()})
                    break
        return found
