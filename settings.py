import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Hmpyjv347&')
BLOG_DATABASE_NAME = 'blog'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{BLOG_DATABASE_NAME}"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = os.path.join('static', 'uploads')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
