from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

api_v1_patterns = (
    [
        path("authenticate/token/", obtain_jwt_token),
        path("authenticate/refresh/", refresh_jwt_token),
        path("feeds/", include("badfeed.feeds.api.urls")),
        path("my/", include("badfeed.users.api.urls")),
    ],
    "api_v1",
)

urlpatterns = [path("admin/", admin.site.urls), path("api/v1/", include(api_v1_patterns))]

urlpatterns += [path("django-rq/", include("django_rq.urls"))]
