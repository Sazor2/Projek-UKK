import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kuncirahasia'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ppdb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # New config
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
