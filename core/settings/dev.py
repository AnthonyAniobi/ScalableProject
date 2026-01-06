from .common import *
import os
from dotenv import load_dotenv
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = ['*',]

# setup for media images
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '/media')

# Static files
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR/ 'static']
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/') 

BASE_URL = '127.0.0.1:8000'
