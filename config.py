import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user_unilink:yourpassword@localhost:5432/unilink_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    FIREBASE_CERT_PATH = os.path.join(os.path.dirname(__file__), "firebase_service.json")
