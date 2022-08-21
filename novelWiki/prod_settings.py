import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-u)dsfyetvbh2dhfu+g(#!doug7b$3&553!$w)@aas@r7l*dgn!%'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", 'novelearn.ru', 'novelearn.ai-info.ru', 'www.novelearn.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'c21535_novelearn_ru',
        'USER': 'c21535_novelearn_ru',
        'PASSWORD': 'KaKyaCulgoyew94',
        'HOST': 'postgres.c21535.h2',
        'PORT': '5432',
    }
}

DB_CONNECTION_STRING="postgresql://c21535_novelearn_ru:KaKyaCulgoyew94@postgres.c21535.h2/c21535_novelearn_ru"

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')