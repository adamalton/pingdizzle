# Standard Library
import math
import time
from urllib.parse import urlencode

# Third Party
from djangae.tasks.decorators import task_or_superuser_only
from djangae.tasks.deferred import defer
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests

# Pingdizzle
from pingapp.globs import (
    TIME_PERIODS,
    NUM_ATTEMPTS_BEFORE_ALERTING,
    ADDITIONAL_BACKOFF_SECONDS_PER_RETRY,
)
from pingapp.utils import report_down


def index(request):
    """Home page. Just info about the app."""
    return render(request, "pingapp/index.html")


@task_or_superuser_only
def spawn_pings(request, frequency):
    """Looks at the config of sites to ping and spawns a task to ping each one."""
    urls_to_ping = settings.PINGCONF[frequency]
    # We want to spread out our tasks so that they don't all run at once and take us
    # over the free App Engine quota.  Pay money?!  Never!  So we spread them out
    # evenly over the hour/day.
    if not urls_to_ping:
        return HttpResponse("No URLs to ping")
    interval = math.floor(float(TIME_PERIODS[frequency]) / float(len(urls_to_ping)))
    delay = 0
    for url in urls_to_ping:
        defer(do_ping, url, _countdown=delay)
        delay += interval
    return HttpResponse("done")


def do_ping(url, attempt=1):
    """Check the given URL and send an email if it's down."""
    error = None
    try:
        response = requests.get(url, timeout=60)
    except requests.RequestException as e:
        error = e
    else:
        status_code = str(response.status_code)
        if status_code[0] not in ("2", "3"):
            error = f"Status: {status_code}"
    if error:
        if attempt < NUM_ATTEMPTS_BEFORE_ALERTING:
            delay = attempt * ADDITIONAL_BACKOFF_SECONDS_PER_RETRY
            defer(do_ping, url, attempt + 1, _countdown=delay)
        else:
            report_down(url, error, attempt)
