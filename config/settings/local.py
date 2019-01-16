from .base import *  # noqa

from envparse import env


DEBUG = env.bool("DJANGO_DEBUG", default=True)
CORS_ORIGIN_ALLOW_ALL = True
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
