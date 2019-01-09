from .base import *  # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration
from envparse import env


sentry_sdk.init(dsn=env.str("SENTRY_DSN", default=""), integrations=[DjangoIntegration(), RqIntegration()])

POCKET_CONSUMER_KEY = env.str("POCKET_CONSUMER_KEY")
