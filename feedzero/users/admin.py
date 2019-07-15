from django.contrib import admin

from feedzero.users.models import feedzeroUser, ThirdPartyTokens


@admin.register(feedzeroUser)
class feedzeroUser(admin.ModelAdmin):
    exclude = ("password",)


@admin.register(ThirdPartyTokens)
class ThirdPartyTokensAdmin(admin.ModelAdmin):
    exclude = ("code",)
