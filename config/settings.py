"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
from django.core.exceptions import ImproperlyConfigured

from django.contrib.messages import constants as messages

# SENTRY
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    USE_CELERY_REDIS=(bool, False)
)
# reading .env file
environ.Env.read_env()

# SENTRY
# sentry_sdk.init(
#     dsn=env('SENTRY_DSN'),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True,
#     # debug=True will work even if the DEBUG=False in Django.
#     debug=True
# )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = env('SECRET_KEY')
except ImproperlyConfigured as e:
    raise ImproperlyConfigured(
        "You are seeing this because, you need to set SECRET_KEY from settings.py file ",
        "or config/.env file. If you don't have this file, create it."
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',  # must be on top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth required
    'django.contrib.sites',
    
    # custom apps
    'students',
    'teachers',
    'result',
    'academics',
    'pages',
    'articles',
    'institute',

    # third party apps
    'crispy_forms',
    'debug_toolbar',
    'rolepermissions',
    'taggit',
    'django_extensions',
    'django_filters',
    'allauth',
    'allauth.account',
    'django_rename_app',
    'allauth.socialaccount',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'widget_tweaks',
    'django_social_share',
    'django_countries',
    'import_export',
    'admin_honeypot',
]

SITE_ID = 1

# for permission management
ROLEPERMISSIONS_MODULE = 'academics.roles'
# ROLEPERMISSIONS_REGISTER_ADMIN = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware to provide institute data in req-resp cycle
    # No longer required since 'attach_institute_data_ctx_processor'
    # context-processor taken place.
    # 'institute.middleware.AttachInstituteDataMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ctx processeor to attach institute data in templates
                'context_processors.dj_sms_context_processor.attach_institute_data_ctx_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db(),
    'extras': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = 'ck-uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ['codesnippet', 'markdown'], 'width': '100%',
    },
}

# authentication stuffs
# from .email_details import *

# TODO:USE YOUR OWN EMAIL SETTINGS FILE 
# for referrence, check the video tutorial link bellow
# https://www.youtube.com/watch?v=51mmqf5a0Ss
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

if 'console' not in EMAIL_BACKEND.split('.'):
    try:
        EMAIL_HOST = env('EMAIL_HOST')
        EMAIL_PORT = env('EMAIL_PORT')
        EMAIL_HOST_USER = env('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    except ImproperlyConfigured as e:
        raise ImproperlyConfigured(
            'Please complete email settings from config/.env file.'
            'If you wan\'t to use smtp mail, you must configure it.'
            'If you want no hassle setting up mail backends, Update'
            'EMAIL_BACKEND to django.core.mail.backends.console.EmailBackend'
        )

# login/register redirects
# LOGIN_REDIRECT_URL = 'index_view'
LOGIN_REDIRECT_URL = 'account:profile_complete'
LOGOUT_REDIRECT_URL = 'account_login'

# LOGIN_URL = 'account:login'
LOGIN_URL = 'account:profile_complete'
LOGOUT_URL = 'account_logout'

# STOP SENDING EMAIL FOR USER REGISTRATION
ACCOUNT_EMAIL_VERIFICATION = 'none'   # use 'mandatory' or 'optional' for respective cases.

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', '*']

# Django taggit.
TAGGIT_CASE_INSENSITIVE = True

# BRAINTREE FOR HANDLING PAYMENTS
try:
    BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
    BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
    BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')
except ImproperlyConfigured as e:
    raise ImproperlyConfigured(
        "Please enter you Braintree sandbox credentials in settings.py or config/.env file."
        "Visit this url if you don't have a sandbox account: https://sandbox.braintreegateway.com/login"
    )

# CELERY BROKER CONFIG
# If you're wishing to update this variable, better update it
# from the config/.env file.
USE_CELERY_REDIS = env('USE_CELERY_REDIS')

if USE_CELERY_REDIS:
    try:
        CELERY_BROKER_URL = env('CELERY_BROKER_URL')
        CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'Asia/Dhaka'
    except ImproperlyConfigured as e:
        raise ImproperlyConfigured(
            'This project uses celery/redis.'
            'If your\'re hearing these names first time, you can '
            'skip this settings by setting USE_CELERY_REDIS=False variable in settings.py.'
            'Otherwise, configure these as described '
            'here: https://github.com/TareqMonwer/Django-School-Management#celery-redis-setup'
        )
