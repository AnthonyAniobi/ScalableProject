from .common import *
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True

INSTALLED_APPS +=['storages']

ALLOWED_HOSTS = ['*'] 

# CORS_ALLOW_ALL_ORIGINS = True  

# ALLOWED_HOSTS = [
#     '127.0.0.1',
#     'localhost',
#     '13.48.134.225',
#     'scalable.thankfulground-41ada081.swedencentral.azurecontainerapps.io',
# ] 

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://13.48.134.225",
    "https://scalable.thankfulground-41ada081.swedencentral.azurecontainerapps.io",
]

# Allow all origins (temporary - development only!)
CORS_ALLOW_ALL_ORIGINS = True

# Allow credentials
CORS_ALLOW_CREDENTIALS = True

# Allow all methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Allow all headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USERNAME'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "anontechnologies.global@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# azure bucket setup
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "timeout": 20,
        }
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "timeout": 20,
        }
    },
}

AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')

# For media files
MEDIA_URL = f'https://eventsasstorage.blob.core.windows.net/eventsascontainer/media/'
# For static files (CSS, JS, images)
STATIC_URL = f'https://eventsasstorage.blob.core.windows.net/eventsascontainer/static/'
