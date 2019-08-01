from envparse import env

from .base import *  # noqa


ALLOWED_HOSTS = env.bool("DJANGO_ALLOWED_HOSTS", default=["*"])
DEBUG = env.bool("DJANGO_DEBUG", default=True)
RQ_ENABLED = env.bool("RQ_ENABLED", default=False)

WEBPACK_LOADER["DEFAULT"]["STATS_FILE"] = os.path.join(
    FRONTEND_DIR, "webpack-stats-dev.json"
)
