"""Configuration management for the medical Text-to-SQL system."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # Database configuration
    DB_TYPE: str = os.getenv("DB_TYPE", "postgresql")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "mimic_demo")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    
    # LLM configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_API_BASE: str = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Application settings
    MAX_RESULT_ROWS: int = int(os.getenv("MAX_RESULT_ROWS", "1000"))
    ENABLE_SQL_RETRY: bool = os.getenv("ENABLE_SQL_RETRY", "true").lower() == "true"
    MAX_RETRY_COUNT: int = int(os.getenv("MAX_RETRY_COUNT", "2"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        if self.DB_TYPE == "postgresql":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Unsupported database type: {self.DB_TYPE}")


config = Config()
