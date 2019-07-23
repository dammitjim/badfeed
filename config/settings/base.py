import os

from envparse import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY", default="wlk9!mepu*mp$^yj-bo2on4)4fj60#(zbzw+@te54xu((b(dfp"
)
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "social_django",
    "django_rq",
    "rest_framework",
    "webpack_loader",
    # internal
    "feedzero.users",
    "feedzero.feeds",
    "feedzero.ingest",
    "feedzero.rules",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "feedzero.feeds.middleware.FeedMenuMiddleware",
]

ROOT_URLCONF = "feedzero.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "..", "feedzero", "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "feedzero.core.context_processors.search_term_processor",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("DATABASE_NAME", default="feedzero_dev"),
        "USER": env.str("DATABASE_USER", default="postgres"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=""),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
    }
}

AUTH_USER_MODEL = "users.FeedZeroUser"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTHENTICATION_BACKENDS = {
    "feedzero.users.backends.Auth0",
    "django.contrib.auth.backends.ModelBackend",
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default="")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "frontend", "theme", "dist", "assets"),
    os.path.join(FRONTEND_DIR, "new", "dist"),
]

MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default="")

RQ_ENABLED = env.bool("RQ_ENABLED", default=True)
RQ_QUEUES = {
    "default": {
        "HOST": env.str("REDIS_HOST", default="localhost"),
        "PORT": env.int("REDIS_PORT", default=6379),
        "DB": env.int("REDIS_DB", default=0),
        "PASSWORD": env.str("REDIS_PASSWORD", default=""),
        "DEFAULT_TIMEOUT": 360,
    }
}


POCKET_CONSUMER_KEY = env.str("POCKET_CONSUMER_KEY", default="")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = env.str("SOCIAL_AUTH_AUTH0_DOMAIN", default="")
SOCIAL_AUTH_AUTH0_KEY = env.str("SOCIAL_AUTH_AUTH0_KEY", default="")
SOCIAL_AUTH_AUTH0_SECRET = env.str("SOCIAL_AUTH_AUTH0_SECRET", default="")
SOCIAL_AUTH_AUTH0_SCOPE = ["openid", "profile"]

LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login"

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "/dist/",  # must end with slash
        "STATS_FILE": os.path.join(FRONTEND_DIR, "webpack-stats-prod.json"),
    }
}
