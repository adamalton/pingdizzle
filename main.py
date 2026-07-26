import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pingsite.settings")

from google.appengine.api import wrap_wsgi_app

from pingsite.wsgi import application

# `wrap_wsgi_app` installs the middleware that makes the legacy bundled services
# (Task Queue, Mail, App Identity) available during each request. `gunicorn`
# serves this `app` object (see the entrypoint in app.yaml).
app = wrap_wsgi_app(application)


import os

# We set the DJANGO_SETTINGS_MODULE here because main.py is only the entry point on a deployed site
# and doesn't get used locally.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apisite.settings.production")
