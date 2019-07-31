# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin

from feedzero.feeds.models import (
    Author,
    Enclosure,
    EnrichedContent,
    Entry,
    EntryState,
    Feed,
    Tag,
)
from feedzero.ingest.jobs import sync_feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "link",
        "date_last_scraped",
        "date_created",
        "date_modified",
    )
    list_filter = ["date_created", "date_modified", "date_last_scraped"]
    search_fields = ["title"]
    actions = ["sync_feeds"]

    def sync_feeds(modeladmin, request, queryset):
        """Manual action to sync the requested feeds."""
        for feed in queryset:
            if settings.RQ_ENABLED:
                sync_feed.delay(feed)
            else:
                sync_feed(feed)

    sync_feeds.short_description = "Queue sync."


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "link",
        "feed",
        "date_published",
        "date_created",
        "date_modified",
    )
    list_filter = ("date_created", "date_modified", "date_published", "feed")
    search_fields = ("title",)
    ordering = ("-date_published",)


@admin.register(EntryState)
class EntryStateAdmin(admin.ModelAdmin):
    pass


@admin.register(EnrichedContent)
class EnrichedContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    list_display = ("href", "file_type", "entry")
    list_filter = ("entry",)
    ordering = ("-entry__date_published",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("term", "scheme", "feed")
    list_filter = ("feed",)
    ordering = ("term",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "link", "feed")
    list_filter = ("feed",)
    ordering = ("name",)
