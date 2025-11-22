# bitkiprojesi/settings.py

from pathlib import Path
import os  

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent # << BURAYI KONTROL ETTİK >>


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jatbn)i6)m^b2!v(10)&(*w1p9a^-!awa&9gws!)t*j34&_o0#' # Kendi anahtarınız kalmalı

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Proje Uygulamaları 
    'bitkiler',
    'tanima',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # E410 hatası için:
    'django.contrib.sessions.middleware.SessionMiddleware', 
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # E408 hatası için:
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    
    # E409 hatası için:
    'django.contrib.messages.middleware.MessageMiddleware', 
    
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bitkiprojesi.urls'

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

WSGI_APPLICATION = 'bitkiprojesi.wsgi.application'


# Database (Aynı kalır)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation (Aynı kalır)
# ...

# Internationalization (Aynı kalır)
# ...

# Static files (Aynı kalır)
STATIC_URL = 'static/'

# Default primary key field type (Aynı kalır)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Medya Ayarları (Kullanıcı tarafından yüklenen dosyalar)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'