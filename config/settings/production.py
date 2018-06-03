from .base import *  # noqa

import os

from envparse import env
import raven


INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
RAVEN_CONFIG = {"dsn": env.str("SENTRY_DSN"), "release": raven.fetch_git_sha(os.path.dirname(BASE_DIR))}
