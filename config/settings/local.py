from .base import *  # noqa

from envparse import env


DEBUG = env.bool("DJANGO_DEBUG", default=True)
if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.SessionAuthentication")
