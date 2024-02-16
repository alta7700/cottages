import os
from pathlib import Path

import phonenumbers
from dotenv import load_dotenv


load_dotenv(override=True)
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ.get('DEBUG', 'true') == 'true'

# example.ru,example2.ru
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', '').split(',') if host]
# https://example.ru,https://example2.ru
CSRF_TRUSTED_ORIGINS = [host for host in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if host]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'homes.apps.HomesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Cottages.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Cottages.wsgi.application'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = False

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
HOME_COVERS_FOLDER = 'home/covers'
HOME_CAROUSEL_IMAGES_FOLDER = 'home/carousel'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

PHONENUMBER_DEFAULT_REGION = 'RU'
PHONENUMBER_DEFAULT_FORMAT = 'E164'

ORGANIZATION_NAME = os.environ['ORGANIZATION_NAME']
ORGANIZATION_PHONES = [
    phonenumbers.parse(phone, 'RU', True)
    for phone in os.environ['ORGANIZATION_PHONES'].split(',') if phone
]
ORGANIZATION_MAIN_PHONE = ORGANIZATION_PHONES[0]
ORGANIZATION_INSTAGRAM = os.environ['ORGANIZATION_INSTAGRAM']
ORGANIZATION_MAILS = tuple(mail.strip() for mail in os.environ.get('ORGANIZATION_MAILS', '').split(',') if mail)

GENERAL_MAP = os.environ['GENERAL_MAP']
YANDEX_VERIFICATION = os.environ['YANDEX_VERIFICATION']
