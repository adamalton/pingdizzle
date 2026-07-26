from django.urls import include, path

from pingapp import views

urlpatterns = [
    path("_ah/", include("djangae.urls")),
    path("_tasks/", include("djangae.tasks.urls")),
    path("", views.index, name="index"),
    path("spawn_pings/<str:frequency>/", views.spawn_pings, name="spawn_pings"),
]
