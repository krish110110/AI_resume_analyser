from docx import Document


class DocxExtractor:
    @staticmethod
    def extract(path: str) -> str:
        doc = Document(path)
        return "\n".join(para.text for para in doc.paragraphs)
