"""
Django settings for example project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT=os.path.dirname(os.path.abspath(__file__))
MAIN_MODULE_NAME=os.path.basename(PROJECT_ROOT)
BASE_DIR = os.path.dirname(PROJECT_ROOT)
URLCOMPASS_DIR=os.path.dirname(os.path.dirname(BASE_DIR)) # need for static location
URLCOMPASS_DIR_NAME=os.path.basename(URLCOMPASS_DIR)
APPS_DIR_NAME='apps'
APPS_DIR=os.path.join(BASE_DIR, APPS_DIR_NAME) # need for static location
TEMPLATES_DIR=os.path.join(BASE_DIR, 'templates')
MEDIA_DIR=os.path.join(BASE_DIR, 'media')

import sys
sys.path.append(URLCOMPASS_DIR)
sys.path.append(APPS_DIR)

print('URLCOMPASS_DIR', URLCOMPASS_DIR)
print('APPS_DIR', APPS_DIR)

APPS=['compass',]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lj)4n)mgdm(lzay@)d@j_s4$+c-#t$&(m%k6#j%fq#zgwlcx$z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

REQUIRED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'urlcompass',
]

PROJECT_APPS = [
    MAIN_MODULE_NAME,
]
for app in APPS:
    PROJECT_APPS.append('.'.join([APPS_DIR_NAME, app,])) 
   
INSTALLED_APPS=REQUIRED_APPS+PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

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

WSGI_APPLICATION = 'example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

URLCOMPASS={  'root_name':'example',
              'start':'[&nbsp',
              'end':'&nbsp]',
              'sep':'&nbsp>&nbsp',
              'html_id': 'example',
              'html_class':'compass_bar',
              'rename': lambda x: x.replace('_', ' ')
}