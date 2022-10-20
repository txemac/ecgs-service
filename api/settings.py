import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "api_secret_key_test")

# SQL database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/ecg_service")
