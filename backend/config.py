import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Server Configuration
    PORT = int(os.getenv('PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5242880))  # 5MB in bytes
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'txt,pdf,docx').split(','))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,https://resumeranker7.netlify.app').split(',')
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True) 