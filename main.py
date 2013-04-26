import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pingsite.settings")
from django.core.handlers.wsgi import WSGIHandler


handler = WSGIHandler()
