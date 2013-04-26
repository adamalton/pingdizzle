from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pingapp.views',
    url(r"^spawn_pings/([A-Z]+)/$", "spawn_pings", name="spawn_pings"),
    url(r"^do_ping/$", "do_ping", name="do_ping"),
)
