"""
Django settings for _LGM project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

ENV = os.environ.get('ENV', 'dev')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# for vue.js spa development
CORS_ALLOWED_ORIGINS = [
    # Vue.js site
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure- change this later')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = str(os.environ.get('DEBUG')) == "1"

ALLOWED_HOSTS = ['127.0.0.1']
if DEBUG:
    ALLOWED_HOSTS += [os.environ.get('ALLOWED_HOST')]


INSTALLED_APPS = [
    'django_silly_stripe',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_silly_auth',

    # local
    '_users',
    'campain_books',
    'subscriptions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '_LGM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = '_LGM.wsgi.application'

#
# CSRF_TRUSTED_ORIGINS = ['http://*']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}


## Site's email config
EMAIL_IS_CONFIGURED = False

if EMAIL_IS_CONFIGURED:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# for testing email easily and free: https://mailtrap.io/
EMAIL_HOST = "mail03.lwspanel.com"
EMAIL_HOST_USER = "no-reply@xxxxxx.fr"
EMAIL_HOST_PASSWORD = "xxxxxx"
EMAIL_PORT = 587
# TLS/SSL is better on if available, otherwise keep it off
EMAIL_USE_TLS = 0

AUTH_USER_MODEL = '_users.User'

SILLY_AUTH = {
    "SITE_NAME": "RPGAdventure.eu",
    "AUTO_SET": "SPA",
    "SPA_EMAIL_LOGIN_LINK": "http://localhost:8080/?#/login_from_email/",
    "USER_INFOS_EXCLUDE": [
        'password', 'is_superuser', 'is_staff', 'is_active', 'new_email',
        'groups', 'user_permissions', 'last_login', 'is_confirmed',
        'first_name', 'last_name',
    ]
}

SILLY_STRIPE = {
    'AUTO_SET': 'SPA',  # 'CLASSIC' or 'SPA'
    'USE_SUBSCRIPTIONS_CANCEL': False,
    'DSS_SECRET_KEY': os.environ.get('DSS_SECRET_KEY'),
    'DSS_PUBLIC_KEY': os.environ.get('DSS_PUBLIC_KEY'),
    # 'DSS_RESTRICTED_KEY': 'rk_xxxxxx',  # optionnal
    'DSS_WEBHOOK_SECRET': os.environ.get('DSS_WEBHOOK_SECRET'),
    'SUBSCRIPTION_CANCEL': 'NOW',  # 'NOW' or 'PERIOD'
    'SUCCESS_URL': 'http://localhost:8080/?#/account',
    'CANCEL_URL': 'http://localhost:8080/?#/account',
    'PORTAL_BACK_URL': 'http://localhost:8080/?#/account',
    # 'PRINT_DEV_LOGS': True,

}
