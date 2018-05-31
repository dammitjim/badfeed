from django.contrib import admin

from .models import BadFeedUser


@admin.register(BadFeedUser)
class BadFeedUser(admin.ModelAdmin):
    exclude = ("password",)
