from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/authenticate/token/", obtain_jwt_token),
    path("api/v1/authenticate/refresh/", refresh_jwt_token),
    path("api/v1/feeds/", include("badfeed.feeds.urls")),
]

urlpatterns += [path("django-rq/", include("django_rq.urls"))]
