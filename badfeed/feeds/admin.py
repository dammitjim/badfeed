# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Feed, Entry, Media


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "url",
        "date_last_scraped",
        "date_created",
        "date_modified",
    )
    list_filter = ("date_created", "date_modified", "date_last_scraped")
    search_fields = ("name",)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "feed",
        "date_first_published",
        "date_created",
        "date_modified",
    )
    list_filter = ("date_created", "date_modified", "date_first_published", "feed")
    search_fields = ("name",)
    ordering = ("-date_first_published",)


# @admin.register(EntryState)
# class UserEntryStateAdmin(admin.ModelAdmin):
#     pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("url", "type", "entry")
    list_filter = ("entry",)
