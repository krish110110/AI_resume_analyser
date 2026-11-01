from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    mongo_url: str = "mongodb://localhost:27017"
    mongo_db_name: str = "ai_resume_analyzer"
    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    upload_dir: str = "storage/uploads"
    reports_dir: str = "storage/generated_reports"
    max_upload_size_mb: int = 10
    allowed_extensions: str = "pdf,docx"
    spacy_model: str = "en_core_web_sm"
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    faiss_index_path: str = "ml/artifacts/faiss/index.faiss"
    admin_email: str = "admin@example.com"
    admin_password: str = "admin123"
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    api_v1_str: str = "/api/v1"


settings = Settings()
