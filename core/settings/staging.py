from util.secret_keys import *
from .common import *

DEBUG = True

SECRET_KEY = DJANGO_SECRET_KEY

ALLOWED_HOSTS = ['*'] 

CORS_ALLOW_ALL_ORIGINS = True  

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# email setup
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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

AZURE_CONTAINER = AZURE_CONTAINER
AZURE_ACCOUNT_NAME = AZURE_ACCOUNT_NAME
AZURE_ACCOUNT_KEY = AZURE_ACCOUNT_KEY

# For media files
MEDIA_URL = f'https://eventsasstorage.blob.core.windows.net/eventsascontainer/media/'
# For static files (CSS, JS, images)
STATIC_URL = f'https://eventsasstorage.blob.core.windows.net/eventsascontainer/static/'
