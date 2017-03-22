"""
Django settings for commons_campaign_commander project.
"""

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('django_secret')

DEBUG = True

ALLOWED_HOSTS = [
    'tools.wmflabs.org',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'social_django',
    'rest_framework',
    'rest_framework_gis',
    'commander',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'commons_campaign_commander.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'commons_campaign_commander.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('db_name'),
        'USER': os.environ.get('db_user'),
        'PASSWORD': os.environ.get('db_password'),
        'HOST': os.environ.get('db_host'),
        'PORT': os.environ.get('db_port')
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.mediawiki.MediaWiki',
    'django.contrib.auth.backends.ModelBackend',
)

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

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

SOCIAL_AUTH_MEDIAWIKI_KEY = os.environ.get('mw_key')
SOCIAL_AUTH_MEDIAWIKI_SECRET = os.environ.get('mw_secret')
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = os.environ.get('mw_callback')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'home'
STATIC_URL = os.environ.get('static_url')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

