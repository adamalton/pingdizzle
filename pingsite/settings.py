import os
from google.appengine.api.app_identity import get_application_id

DEBUG = "/Users/" in __file__ #On OS X
TEMPLATE_DEBUG = DEBUG

APP_ID = get_application_id()

SECRET_KEY = '5te0=AhDvfgHU*&Jw(rm$INFC8MnZT7lspoubL-1jB3c+x2WKk'

ADMINS = [
    ('Adam Alton', 'adamalton@gmail.com'),
]

INSTALLED_APPS = (
    # ** GENERIC / DJANGO STUFF **
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    #'django.contrib.admin',

    #My STUFF
    'pingsite',
    'pingapp',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATIC_URL = '/static/'

ROOT_URLCONF = 'pingapp.urls'


MIDDLEWARE_CLASSES = (
    #Django defaults
    #'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #Django
    #"django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    #"django.core.context_processors.media",
    "django.core.context_processors.request",
    #"django.contrib.messages.context_processors.messages",
    )

DEFAULT_FROM_EMAIL = "Pingdizzle <noreply@%s.appspotmail.com>" % APP_ID
SERVER_EMAIL = DEFAULT_FROM_EMAIL


PINGCONF = {
    'HOURLY': [
        'http://adamalton.co.uk',
        'https://adamalton.com',
        'http://kowethastringquartet.co.uk',
        'http://marcherfencing.co.uk',
        'http://www.tmtotnes.co.uk',
        'http://rechar.gr',
        'https://twistpass.com',
    ],
    'DAILY': [
    ]
}

SEND_DOWNTIME_NOTIFICATIONS_T0 = ADMINS


try:
    from local_settings import *
except ImportError:
    pass
