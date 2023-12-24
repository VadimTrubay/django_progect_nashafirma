from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = '#iqnq9p2w(47tmqwuh_s+ot$)tov9bh%(=dxfj5as)u&2pts'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_totals",
    "captcha",
    "orders.apps.OrdersConfig",
    "products.apps.ProductsConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = "nashafirma.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.i18n',
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nashafirma.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": str(os.path.join(BASE_DIR, "db.sqlite3")),
#     }
# }
"""Local PostgresSQL"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nashafirma',
        'USER': 'nashafirma',
        'PASSWORD': 'vad0101vad',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# """Local MySQL"""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'nashafirmaod_db',
#         'USER': 'nashafirmaod_db',
#         'PASSWORD': 'Q(Zh_HV#Qf5M',
#         'HOST': 'localhost',   # Set to your database host
#         'PORT': '3306',        # Set to your database port
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'charset': 'utf8mb4'
#         },
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = (
    ('uk', 'Ukrainian'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

LANGUAGE_CODE = "uk"

TIME_ZONE = "Europe/Kiev"

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = ('locale',)

STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "static",)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.SiteUser"

LOGIN_URL = 'users'

"""For Gmail"""
EMAIL_ADMIN = 'user0606user@gmail.com'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_STARTTLS = True
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'user0606user@gmail.com'
EMAIL_HOST_PASSWORD = 'jezyscoekirdwblv'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CAPTCHA_FONT_SIZE = 33
CAPTCHA_LENGTH = 3
# CAPTCHA_LETTER_ROTATION = -66, 66
