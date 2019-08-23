from envparse import env
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration

from .base import *  # noqa


sentry_init(
    dsn=env.str("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration(), RedisIntegration(), RqIntegration()],
)

POCKET_CONSUMER_KEY = env.str("POCKET_CONSUMER_KEY")

STATICFILES_DIRS = [os.path.join(FRONTEND_DIR, "theme", "dist", "assets")]
