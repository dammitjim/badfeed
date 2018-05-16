from .base import *  # noqa

from envparse import env


DEBUG = env.bool('DJANGO_DEBUG', default=True)
