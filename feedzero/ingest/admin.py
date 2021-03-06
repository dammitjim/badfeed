from django.contrib import admin

from feedzero.ingest.models import IngestLog


@admin.register(IngestLog)
class IngestLogAdmin(admin.ModelAdmin):
    list_display = ("state", "date_created", "feed")
    list_filter = ("feed", "state")
