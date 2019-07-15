from django.contrib import admin

from feedzero.users.models import FeedZeroUser, ThirdPartyTokens


@admin.register(FeedZeroUser)
class FeedZeroUser(admin.ModelAdmin):
    exclude = ("password",)


@admin.register(ThirdPartyTokens)
class ThirdPartyTokensAdmin(admin.ModelAdmin):
    exclude = ("code",)
