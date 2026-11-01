from datetime import datetime


class DateUtils:
    @staticmethod
    def now() -> datetime:
        return datetime.utcnow()
