import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration de BourSignal."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = True

    # MySQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "boursignal")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    # Finnhub API
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
    FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

    # Envoi d'emails (SMTP). Si SMTP_USER/SMTP_PASSWORD sont vides,
    # le service bascule en "mode dev" : il logue le mail au lieu de l'envoyer.
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "") or SMTP_USER

    # URL du front, pour construire le lien de gestion envoyé par email.
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class TestConfig(Config):
    """Configuration utilisée par la suite pytest."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    FINNHUB_API_KEY = "test-key"
