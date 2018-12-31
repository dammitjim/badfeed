from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/django-rq/", include("django_rq.urls")),
    path("", include("badfeed.feeds.urls")),
    path("", include("badfeed.users.urls")),
]
