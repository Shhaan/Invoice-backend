
from pathlib import Path
import os
import dj_database_url
 
BASE_DIR = Path(__file__).resolve().parent.parent

 


SECRET_KEY = 'django-insecure-+51d#21@u3#bm(w081$wzn44zfxnss6^p5hej8^0)7c$jab!gh'
 
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app','127.0.0.1']

  
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000/'
]


INSTALLED_APPS = [
    'jazzmin',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
   'rest_framework.authtoken',
    "cloudinary",
    "cloudinary_storage",
    'cookieapp',
    'main',
    'invoice'

    
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

ROOT_URLCONF = 'backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS' : [
            os.path.join(BASE_DIR, "invoice", "template"),
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

 
  
DB_URL = 'postgresql://postgres:TmbMgAwTAyZqAXgKztBjxiSuhBPUcwNW@maglev.proxy.rlwy.net:12202/railway'
DATABASES = {
    'default': dj_database_url.config(default=DB_URL, conn_max_age=1800)
}
 
 

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dl1qukeww',
    'API_KEY': '398438651375956',
    'API_SECRET': 'R7nVCIw6M5gaAQRvi_-NNopPPDE',
}



REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  
    ],
      'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


 
 

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


 
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

AUTH_USER_MODEL = "cookieapp.Account"
  