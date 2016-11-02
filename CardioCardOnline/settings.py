"""
Django settings for CardioCardOnline project.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'a=bq4gjswb@ppr5q+ouwm+po!%&6!gabc^b&$*sq31-m=^ng1t'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cconline.templatetags',
    'cconline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300
    }
}

ROOT_URLCONF = 'CardioCardOnline.urls'

ROOTDIR = os.path.abspath(os.path.dirname(__file__))

#TEMPLATE_DIRS = (
#    ROOTDIR + 'CardioCardOnline\templates',
#)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            #ROOTDIR + '/CardioCardOnline/templates'
            '/var/www/cconline/CardioCardOnline/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'CardioCardOnline.wsgi.application'

# Database
# Firebird
# for high load need set CONN_MAX_AGE not 0.

DATABASES = {
    'default': {
        'ENGINE': 'firebird',
        'HOST': 'labgsrv',
        'NAME': 'cardiocard',
        'PORT': '3050',
        'USER': 'SYSDBA',
        'PASSWORD': 'Monstro13',
        'CONN_MAX_AGE': None,
    }
}

# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

DEFAULT_INDEX_TABLESPACE = ''
