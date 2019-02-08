from django.contrib import admin

from badfeed.users.models import BadFeedUser, ThirdPartyTokens


@admin.register(BadFeedUser)
class BadFeedUser(admin.ModelAdmin):
    exclude = ("password",)


@admin.register(ThirdPartyTokens)
class ThirdPartyTokensAdmin(admin.ModelAdmin):
    exclude = ("code",)
