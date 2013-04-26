#SYSTEM
import math
from urllib import urlencode

#LIBRARIES
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

#PINGDIZZLE
from pingapp.pingconf import PINGCONF, TIME_PERIODS
from pingapp.utils import report_down


def spawn_pings(request, frequency):
    """ Looks at the config of sites to ping and spawns a task to ping each one. """
    ping_task_url = reverse("do_ping")
    urls_to_ping = PINGCONF[frequency]
    #We want to spread out our tasks so that they don't all run at once and take us
    #over the free App Engine quota.  Pay money?!  Never!  So we spread them out
    #evenly over the hour/day.
    interval = math.floor(float(TIME_PERIODS[frequency]) / float(len(urls_to_ping)))
    delay = 0
    for url in urls_to_ping:
        querystring = urlencode([('url', url)])
        taskqueue.add(
            url="%s?%s" % (ping_task_url, querystring),
            method="GET",
            countdown=delay
        )
        #delay += interval
    return HttpResponse('done')


def do_ping(request):
    """ Check the given URL and send an email if it's down. """
    error = None
    url = request.GET['url']
    try:
        response = urlfetch.fetch(url)
    except urlfetch.DownloadError as e:
        error = e
    else:
        status_code = str(response.status_code)
        if status_code[0] not in ('2', '3'):
            error = status_code
    if error:
        report_down(url, error)
    return HttpResponse('done')
