from envparse import env
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration

from .base import *  # noqa


sentry_init(
    dsn=env.str("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration(), RqIntegration()],
)

POCKET_CONSUMER_KEY = env.str("POCKET_CONSUMER_KEY")

STATICFILES_DIRS = [os.path.join(FRONTEND_DIR, "dist", "entry-widget")]
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": DEBUG,
        "BUNDLE_DIR_NAME": "/entry-widget/",  # must end with slash
        "STATS_FILE": os.path.join(FRONTEND_DIR, "webpack-stats-prod.json"),
    }
}
