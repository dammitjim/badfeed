from django.contrib import admin
from django.urls import include, path


api_urlpatterns = [path("feeds/", include("badfeed.feeds.api.urls"))]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/django-rq/", include("django_rq.urls")),
    path("", include("badfeed.feeds.urls")),
    path("", include("badfeed.users.urls")),
    # TODO this probably includes too many, have a gander at it
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    path("api/v1/", include(api_urlpatterns)),
]
