import os
from djangae.contrib.secrets import get as get_secrets
from djangae.environment import is_production_environment, project_id
from djangae.settings_base import *  # pylint:disable=wildcard-import,unused-wildcard-import

# On the App Engine Python 3 runtime the local file path won't contain
# "/Users/", so DEBUG is automatically off in production.
DEBUG = not is_production_environment()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The second-generation runtime exposes the project ID via this env var.
APP_ID = project_id()

SECRET_KEY = get_secrets().secret_key if is_production_environment() else "dev-secret-key"

# App Engine terminates requests behind its front end, so accepting any host is
# fine here. Restrict this if you serve the app under a custom domain.
ALLOWED_HOSTS = ["*"]

ADMINS = [
    (
        "Adam Alton",
        "x".join(["m", "e", "@", "a", "d", "a", "m", "a", "l", "t", "o", "n", ".", "c", "o", "m"]).replace("x", ""),
    ),
]

INSTALLED_APPS = [
    "djangae",
    "djangae.contrib.security",
    "djangae.tasks",
    "pingsite",
    "pingapp",
]

MIDDLEWARE = [
    "djangae.contrib.common.middleware.RequestStorageMiddleware",
    "djangae.tasks.middleware.TaskEnvironmentMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "pingapp.urls"

WSGI_APPLICATION = "main.app"


DATASTORE_INDEX_YAML = os.path.join(BASE_DIR, "dsindex.yaml")

DATABASES = {
    "default": {
        "ENGINE": "gcloudc.db.backends.datastore",
        "PROJECT": project_id(),
        "INDEXES_FILE": DATASTORE_INDEX_YAML,
    }
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

STATIC_URL = "/static/"

USE_TZ = True

DEFAULT_FROM_EMAIL = "Pingdizzle <noreply@%s.appspotmail.com>" % APP_ID
SERVER_EMAIL = DEFAULT_FROM_EMAIL


PINGCONF = {
    "HOURLY": [
        "https://adamalton.co.uk",
        "https://adamalton.com",
        "https://app.axiogrow.com",
        "https://www.axiogrow.com",
        "https://marcherfencing.co.uk",
    ],
    "DAILY": [],
}

SEND_DOWNTIME_NOTIFICATIONS_T0 = ADMINS


try:
    from local_settings import *  # noqa: F401,F403
except ImportError:
    pass
