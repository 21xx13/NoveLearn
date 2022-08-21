import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-u)&1d1%ux&n6r1c+g(#!doug7b$3&553!$w)@aas@r7l*dgn!%'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", 'novelearn.ru', 'novelearn.ai-info.ru', 'www.novelearn.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'novelearn',
        'USER': 'postgres',
        'PASSWORD': '21stopium',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
