import os

class Config:
    """Base configuration variables."""
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
        self.LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN')

    