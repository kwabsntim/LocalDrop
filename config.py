import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'LocalDrop')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'xlsx', 'csv', 'zip', 'rar'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    PORT = 3030
    HOST = '0.0.0.0'


# Select config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
