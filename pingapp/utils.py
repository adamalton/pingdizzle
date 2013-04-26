#SYSTEM
import logging

#LIBRARIES
from django.conf import settings
from google.appengine.api import mail


SUBJECT = "[PINGDIZZLE] DOWN: %s"
BODY = """Hi %(name)s,

The URL %(url)s is down.  The error is '%(error)s'.
"""


def report_down(url, error):
    """ Send notifications about a URL being down. """
    subject = SUBJECT % url
    for name, email in settings.SEND_DOWNTIME_NOTIFICATIONS_T0:
        body_args = {
            'url': url,
            'error': error,
            'name': name,
        }
        body = BODY % body_args
        message = mail.EmailMessage(
            sender=settings.DEFAULT_FROM_EMAIL,
            to=email,
            subject=subject,
            body=body
        )
        message.send()
    logging.error("%s is down", url)
