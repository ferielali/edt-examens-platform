"""
Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
Configuration de l'application
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = "Exam Scheduler API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/exam_scheduler"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # JWT Authentication
    SECRET_KEY: str = "your-super-secret-key-change-in-production-minimum-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Allow all origins for Railway deployment
    CORS_ORIGINS: list = ["*"]
    
    # Scheduling Algorithm Settings
    MAX_EXAMS_PER_DAY_STUDENT: int = 1
    MAX_EXAMS_PER_DAY_PROFESSOR: int = 3
    SCHEDULING_TIMEOUT_SECONDS: int = 45
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
