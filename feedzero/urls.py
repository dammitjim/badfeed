from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/django-rq/", include("django_rq.urls")),
    path("", include("feedzero.feeds.urls")),
    path("", include("feedzero.users.urls")),
    # TODO this probably includes too many, have a gander at it
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    path("api/v1/", include("feedzero.api.urls")),
]
