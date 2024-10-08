# from typing import List
# from pydantic import BaseSettings, AnyUrl

# class Settings(BaseSettings):
#     # Common settings
#     PROJECT_NAME: str = "ReportViewer"
#     DEBUG: bool = False
#     SECRET_KEY: str
#     ALLOWED_HOSTS: List[str] = ["*"]

#     # Database settings
#     DATABASE_URL: AnyUrl

#     # Redis settings for Celery
#     REDIS_URL: AnyUrl = "redis://localhost:6379/0"
#     CELERY_BROKER_URL: AnyUrl = REDIS_URL
#     CELERY_BACKEND_URL: AnyUrl = REDIS_URL

#     # Environment-specific settings
#     ENV: str = "development"  # Can be 'development', 'staging', or 'production'

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

# # Define specific settings for development, staging, and production

# class DevelopmentSettings(Settings):
#     DEBUG: bool = True

# class StagingSettings(Settings):
#     DEBUG: bool = False
#     ALLOWED_HOSTS: List[str] = ["staging.yourdomain.com"]

# class ProductionSettings(Settings):
#     DEBUG: bool = False
#     ALLOWED_HOSTS: List[str] = ["yourdomain.com"]

# # Function to get the correct settings based on the environment
# def get_settings() -> Settings:
#     from os import getenv
#     env = getenv("ENV", "development")
    
#     if env == "production":
#         return ProductionSettings()
#     elif env == "staging":
#         return StagingSettings()
#     return DevelopmentSettings()

# # You can access settings like this throughout your FastAPI application
# settings = get_settings()
