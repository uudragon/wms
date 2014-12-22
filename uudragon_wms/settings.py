"""
Django settings for uudragon_wms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import logging.config
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Environment property. include DEV, TEST, PROD
ENV_PROP = 'DEV'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x991kt+hcad8j-s2ux%c!53s08g-=n=r8k2!ipx8m=#-8&=%1i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'big_house',
    'inbound',
    'outbound',
    'inner',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'uudragon_wms.urls'

WSGI_APPLICATION = 'uudragon_wms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = None

if ENV_PROP == 'DEV':
    DATABASES = {
        'default': {
            'NAME': 'wms',
            'ENGINE': 'mysql.connector.django',
            'USER': 'wms_admin',
            'PASSWORD': 'wms_admin',
            'HOST': '192.168.56.101',
            'PORT': '3306',
            'OPTIONS': {
                'autocommit': True,
                },
            }
    }
elif ENV_PROP == 'TEST':
    DATABASES = {
        'default': {
            'NAME': 'wms',
            'ENGINE': 'mysql.connector.django',
            'USER': 'wms_rw',
            'PASSWORD': 'wms_rw',
            'HOST': '119.255.25.130',
            'PORT': '3306',
            'OPTIONS': {
                'autocommit': True,
                },
            }
    }
elif ENV_PROP == 'PROD':
    DATABASES = {
        'default': {
            'NAME': 'wms',
            'ENGINE': 'mysql.connector.django',
            'USER': 'wms_rw',
            'PASSWORD': 'wms_rw',
            'HOST': '119.255.25.130',
            'PORT': '3306',
            'OPTIONS': {
                'autocommit': True,
                },
            }
    }
else:
    raise Exception('The value of ENV_PROP is error. Expect \'DEV\'|\'TEST\'|\'PROD\'.Actual %S' % ENV_PROP)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Logging configuration
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(filename)s-%(lineno)s] -- %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'filters': {
        # 'console.handlers': {
        #     'class': 'logging.Filter',
        #     'name': 'console.handlers',
        # },
    },
    'handlers': {
        'wms': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/uudragon_wms.log',
            'when': 'D',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['wms'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        }
    }

}
logging.config.dictConfig(LOG_CONFIG)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
