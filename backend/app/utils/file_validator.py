import os
from app.core.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


class FileValidator:
    @staticmethod
    def validate(filename: str, size_mb: float) -> None:
        ext = filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"File type .{ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}")
        if size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"File too large ({size_mb}MB). Max {MAX_FILE_SIZE_MB}MB")
