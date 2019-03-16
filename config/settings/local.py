from envparse import env

from .base import *  # noqa


DEBUG = env.bool("DJANGO_DEBUG", default=True)
CORS_ORIGIN_ALLOW_ALL = True
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
RQ_ENABLED = env.bool("RQ_ENABLED", default=False)
