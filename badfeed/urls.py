from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/feeds/", include('badfeed.feeds.urls')),
]

urlpatterns += [path("django-rq/", include("django_rq.urls"))]
