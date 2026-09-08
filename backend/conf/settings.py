"""
Django settings for conf project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv('SECRET_KEY', 'local-development-only-change-me')
DEBUG = os.getenv('DEBUG', 'False').lower() in {'1', 'true', 'yes'}
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CONTENT_GENERATION_PROVIDER = os.getenv('CONTENT_GENERATION_PROVIDER', 'local').lower()
CONTENT_GENERATION_MODEL = os.getenv('CONTENT_GENERATION_MODEL', 'gpt-4o-mini')
CONTENT_GENERATION_BASE_URL = os.getenv('CONTENT_GENERATION_BASE_URL', 'https://api.openai.com/v1')
CONTENT_GENERATION_TIMEOUT = int(os.getenv('CONTENT_GENERATION_TIMEOUT', '20'))
SOCIAL_PUBLISH_MODE = os.getenv('SOCIAL_PUBLISH_MODE', 'simulate').lower()

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'corsheaders',
    # ── REST / Auth Setup ──
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django.contrib.sites',

    # ── Allauth Core ──
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # ── Providers ──
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitter',

    # ── Swagger & Docs ──
    'drf_yasg',

    # ── Your App(s) ──
    'api',
    'accounts',
    'content_generator',
    'social_accounts',
]
SITE_ID = 4

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'conf.wsgi.application'

# config databases
if os.environ.get('DOCKER_ENV'):
    # اگر در Docker باشیم، از PostgreSQL استفاده کن
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
elif os.environ.get('USE_MYSQL') == '1':
    # اگر XAMPP فعال باشد، از MySQL استفاده کن
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME_MYSQL', 'your_database_name'),  # نام پایگاه داده MySQL
            'USER': os.getenv('DB_USER_MYSQL', 'root'),  # کاربر MySQL (معمولاً root)
            'PASSWORD': os.getenv('DB_PASSWORD_MYSQL', ''),  # رمز عبور MySQL (معمولاً خالی)
            'HOST': os.getenv('DB_HOST_MYSQL', 'localhost'),  # آدرس پایگاه داده
            'PORT': os.getenv('DB_PORT_MYSQL', '3306'),  # پورت MySQL (معمولاً 3306)
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Static
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# dj_rest_auth + JWT
REST_AUTH = {
    'USE_JWT': True,  
    'JWT_AUTH_COOKIE': 'jwt-access',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh',
    'JWT_AUTH_HTTPONLY': False,  # برای فرانت‌اند
    'PASSWORD_RESET_USE_SITES_DOMAIN': False,
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'REGISTER_SERIALIZER': 'accounts.serializers.RegisterSerializer',
}

# REST Framework + SimpleJWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',  # existing cookie authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Email (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'OperAGI <noreply@localhost>')

# Google OAuth
GOOGLE_OAUTH_CALLBACK_URL = os.getenv('GOOGLE_OAUTH_CALLBACK_URL')


# Allauth Account Settings
ACCOUNT_LOGIN_METHODS = {'email'}  # فقط با ایمیل
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-requested-with",
]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Allauth + dj-rest-auth اضافی

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
PASSWORD_RESET_CONFIRM_URL = 'reset-password/{uid}/{token}'
ACCOUNT_ADAPTER = 'accounts.adapter.CustomAccountAdapter'
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_EMAIL_VERIFICATION = os.getenv('ACCOUNT_EMAIL_VERIFICATION', 'optional')
# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# Google SCOPE
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'openid',     
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'instagram': {
        'APP': {
            'client_id': os.getenv('INSTAGRAM_CLIENT_ID'),
            'secret': os.getenv('INSTAGRAM_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['user_profile', 'user_media'],
        'AUTH_PARAMS': {'scope': 'user_profile,user_media'},
    },
    'twitter': {
        'APP': {
            'client_id': os.getenv('TWITTER_CONSUMER_KEY'),
            'secret': os.getenv('TWITTER_CONSUMER_SECRET'),
            'key': ''
        },
    },
}


# Celery is optional locally. API code safely falls back when no broker is
# reachable; Docker Compose enables worker and beat processes.
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)
CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', 'True').lower() in {'1', 'true', 'yes'}
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULE = {
    'publish-due-operagi-posts': {
        'task': 'content_generator.tasks.process_due_schedules',
        'schedule': 60.0,
    },
}
