import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "api_secret_key_test")

# SQL database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/ecg_service")

# Auth
AUTH_ACCESS_TOKEN_ALGORITHM = os.getenv("AUTH_ACCESS_TOKEN_ALGORITHM", "HS256")
AUTH_TOKEN_EXPIRE_MINUTES = os.getenv("AUTH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 30)  # 1 month
