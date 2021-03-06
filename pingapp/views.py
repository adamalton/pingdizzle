#SYSTEM
import math
import time
from urllib import urlencode

#LIBRARIES
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

#PINGDIZZLE
from pingapp.globs import (
    TIME_PERIODS,
    NUM_ATTEMPTS_BEFORE_ALERTING,
    ADDITIONAL_BACKOFF_SECONDS_PER_RETRY,
)
from pingapp.utils import report_down


def index(request):
    """ Home page. Just info about the app. """
    return render(request, "pingapp/index.html")



def spawn_pings(request, frequency):
    """ Looks at the config of sites to ping and spawns a task to ping each one. """
    ping_task_url = reverse("do_ping")
    urls_to_ping = settings.PINGCONF[frequency]
    #We want to spread out our tasks so that they don't all run at once and take us
    #over the free App Engine quota.  Pay money?!  Never!  So we spread them out
    #evenly over the hour/day.
    if not urls_to_ping:
        return HttpResponse('No URLs to ping')
    interval = int(math.floor(float(TIME_PERIODS[frequency]) / float(len(urls_to_ping))))
    delay = 0
    for url in urls_to_ping:
        querystring = urlencode([('url', url)])
        taskqueue.add(
            url="%s?%s" % (ping_task_url, querystring),
            method="GET",
            countdown=delay
        )
        delay += interval
    return HttpResponse('done')


def do_ping(request, attempt=1):
    """ Check the given URL and send an email if it's down. """
    error = None
    url = request.GET['url']
    try:
        response = urlfetch.fetch(url, validate_certificate=True)
    except urlfetch.Error as e:
        error = e
    else:
        status_code = str(response.status_code)
        if status_code[0] not in ('2', '3'):
            error = "Status: %s" % status_code
    if error:
        if attempt < NUM_ATTEMPTS_BEFORE_ALERTING:
            time.sleep(attempt * ADDITIONAL_BACKOFF_SECONDS_PER_RETRY)
            do_ping(request, attempt + 1)
        else:
            report_down(url, error, attempt)
    return HttpResponse('done')
