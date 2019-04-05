# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Author, Enclosure, Entry, EntryState, EnrichedContent, Feed, Tag


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
    list_filter = ("date_created", "date_modified", "date_last_scraped")
    search_fields = ("title",)


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
