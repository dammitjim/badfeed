from django.apps import AppConfig


class FeedsConfig(AppConfig):
    name = "feedzero.feeds"

    def ready(self):
        import feedzero.feeds.receivers  # noqa
