from envparse import env

from .base import *  # noqa


DEBUG = env.bool("DJANGO_DEBUG", default=True)
RQ_ENABLED = env.bool("RQ_ENABLED", default=False)
