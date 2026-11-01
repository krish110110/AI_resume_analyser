import fitz


class PdfExtractor:
    @staticmethod
    def extract(path: str) -> str:
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
