from .base import *  # noqa

from envparse import env


INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
RAVEN_CONFIG = {"dsn": env.str("SENTRY_DSN", default="")}
