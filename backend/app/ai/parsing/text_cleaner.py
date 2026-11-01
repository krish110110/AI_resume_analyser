import re


class TextCleaner:
    def clean(self, text: str) -> str:
        # Normalize whitespace but preserve newlines for section detection
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs -> single space
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines -> double newline
        # Remove control characters but keep printable chars and newlines
        text = re.sub(r'[^\w\s@.,:;()\-+/\\n]', '', text)
        return text.strip()
