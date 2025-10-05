import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-replace-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Add token expiration
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)