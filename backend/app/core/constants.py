from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class ResumeStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisType(str, Enum):
    FULL = "full"
    QUICK = "quick"
    ATS_ONLY = "ats_only"


class FileType(str, Enum):
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_FILE_SIZE_MB = 10
