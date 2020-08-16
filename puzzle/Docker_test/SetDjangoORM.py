import django
from django.conf import settings
import os
import sys
sys.path.insert(0,'/')
BASE_DIR = '/'

settings.configure(
    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'db',
                'PORT': 5432,
            }
    },
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'puzzle'
            ]
)
django.setup()
