"""
Django settings for Focus-Power project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import json
import logging
import os
from os import path
from pathlib import Path

from dotenv import load_dotenv
from focus_power.infrastructure.logger.models import AttributeLogger
from focus_power.infrastructure.logger.services import (
    CounterLogFormatter,
    CustomizedJSONFormatter,
)
from logging_utilities.formatters.extra_formatter import ExtraFormatter
from utils.django.exceptions.lazy_exceptions import LazyExceptions

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG", 0)))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

PROJECT_DIR = "focus_power"
# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_extensions",
    "django.contrib.admin",
    "django_filters",
    "debug_toolbar",
    "storages",
    "django_pgviews",
    # app modules
    "focus_power.domain.user",
    "focus_power.domain.user.reportee_tracker",
    "focus_power.domain.company",
    "focus_power.domain.company.company_division",
    "focus_power.domain.division",
    "focus_power.domain.division.user_division",
    "focus_power.domain.objective",
    "focus_power.domain.objective.objectivecondition",
    "focus_power.domain.prioritized_task",
    "focus_power.domain.role",
    "focus_power.domain.role.company_role",
    "focus_power.domain.role.user_role",
    "focus_power.application.roles.apps.ApplicationRoleConfig",
    "focus_power.application.division.apps.ApplicationDivisionConfig",
    "focus_power.domain.kpi",
    "focus_power.domain.kpi.kpi_frequency",
    "focus_power.domain.page_level_permission",
    "focus_power.domain.calender_manager",
    "focus_power.domain.initiative",
    "focus_power.domain.initiative.initiative_action",
    "focus_power.domain.process",
    "focus_power.domain.file",
    "focus_power.domain.recurring_activities",
    "focus_power.domain.recurring_activities.recurring_records",
    "focus_power.domain.forecast",
    "focus_power.domain.document",
    "focus_power.domain.review",
    "focus_power.domain.review.review_settings",
    "focus_power.domain.review.highlight_lowlight",
    "focus_power.domain.review.review_action",
    "focus_power.domain.general_settings",
    "focus_power.domain.general_settings.billing_information",
    "focus_power.domain.planning",
    "focus_power.domain.planning.planning_overview",
    "custom_admin",
    "widget_tweaks",
    "focus_power.domain.direct_report",
    "focus_power.application.objective.apps.ApplicationObjectiveView",
    "focus_power.application.user.apps.ApplicationUserProfileView",
    "focus_power.application.company.apps.ApplicationCompanyDivisionView",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "focus_power.infrastructure.middlewares.api_response_middleware.CustomResponseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "focus_power.interface.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "FocusPower",
    "DESCRIPTION": "An application built to showcase a loose Domain Driven Design implementation in Django",
    "TOS": None,
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {"name": "", "email": ""},
    "VERSION": "0.1.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

WSGI_APPLICATION = "focus_power.drivers.wsgi.application"

AUTH_USER_MODEL = "user.User"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# flag for enable api or disable api

ENABLE_API = False
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


from datetime import date, timedelta

LOGGER_HANDLERS = os.getenv(
    "LOGGER_HANDLERS",
    [
        "debug_file",
        "info_file",
        "warn_file",
        "error_file",
    ],
).split(",")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": CustomizedJSONFormatter,
        },
        "app": {
            "()": ExtraFormatter,
            "format": 'level: "%(levelname)s"\t msg: "%(message)s"\t logger: "%(name)s"\t func: "%(funcName)s"\t time: "%(asctime)s"',
            "datefmt": "%Y-%m-%dT%H:%M:%S.%z",
            "extra_fmt": "\t extra: %s",
        },
        "simple_string": {
            "format": "%(levelname)s %(asctime)s %(message)s\n",
            "datefmt": "%Y-%m-%dT%H:%M:%S.%z",
        },
        "custom_format_with_counter": {
            "()": CounterLogFormatter,
        },
    },
    "handlers": {
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"logs/debug/{date.today()}_logger.log",
            "formatter": "json",
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"logs/info/{date.today()}_info.log",
            "formatter": "json",
        },
        "warn_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": f"logs/warning/{date.today()}_warn.log",
            "formatter": "json",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": f"logs/error/{date.today()}_error.log",
            "formatter": "json",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "db_query_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "custom_format_with_counter",
            "filename": f"logs/db_query/{date.today()}_debug.log",
        },
    },
    "loggers": {
        "": {
            "handlers": LOGGER_HANDLERS,
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["db_query_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

from datetime import timedelta

ACCESS_TOKEN_LIFETIME = int(os.getenv("ACCESS_TOKEN_LIFETIME"))
REFRESH_TOKEN_LIFETIME = int(os.getenv("REFRESH_TOKEN_LIFETIME"))
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = path.join(BASE_DIR, "static").replace("\\", "/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")

ENABLE_MAILS = bool(int(os.getenv("ENABLE_MAILS")))

CLIENT_HOST = os.getenv("CLIENT_HOST")

# add new user
ADD_NEW_USER_SIGN_UP_TEMPLATE = os.getenv("ADD_NEW_USER_SIGN_UP_TEMPLATE")
ADD_NEW_USER_USE_CASE = os.getenv("ADD_NEW_USER_USE_CASE")
ADD_NEW_USER_EXP_TIME = int(os.getenv("ADD_NEW_USER_EXP_TIME"))
ADD_NEW_USER_TOKEN_SECRETE = os.getenv("ADD_NEW_USER_TOKEN_SECRETE")
ADD_NEW_USER_ROUTE = os.getenv("ADD_NEW_USER_ROUTE")
ADD_NEW_USER_SUBJECT = os.getenv("ADD_NEW_USER_SUBJECT")

# Invite CEO
INVITE_CEO_SIGN_UP_TEMPLATE = os.getenv("INVITE_CEO_SIGN_UP_TEMPLATE")

# Invite CEO Assistant
INVITE_CEO_ASSISTANT_SIGN_UP_TEMPLATE = os.getenv(
    "INVITE_CEO_ASSISTANT_SIGN_UP_TEMPLATE"
)

# Invite Success manager
INVITE_SM_SIGN_UP_TEMPLATE = os.getenv("INVITE_SM_SIGN_UP_TEMPLATE")

# Add SM
ADD_SM_USER_TEMPLATE = os.getenv("ADD_SM_USER_TEMPLATE")

# new user verification
NEW_USER_VERIFICATION_EMAIL_TEMPLATE = os.getenv("NEW_USER_VERIFICATION_EMAIL_TEMPLATE")
NEW_USER_VERIFICATION_SECRETE = os.getenv("NEW_USER_VERIFICATION_SECRETE")
NEW_USER_VERIFICATION_EXP_TIME = int(os.getenv("NEW_USER_VERIFICATION_EXP_TIME"))
NEW_USER_VERIFICATION_ROUTE = os.getenv("NEW_USER_VERIFICATION_ROUTE")
NEW_USER_TOKEN_USE_CASE = os.getenv("NEW_USER_TOKEN_USE_CASE")
NEW_USER_SUBJECT = os.getenv("NEW_USER_SUBJECT")

# forgot password
FORGOT_PASSWORD_EMAIL_TEMPLATE = os.getenv("FORGOT_PASSWORD_EMAIL_TEMPLATE")
FORGOT_PASSWORD_SECRETE = os.getenv("FORGOT_PASSWORD_SECRETE")
FORGOT_PASSWORD_EXP_TIME = int(os.getenv("FORGOT_PASSWORD_EXP_TIME"))
FORGOT_PASSWORD_ROUTE = os.getenv("FORGOT_PASSWORD_ROUTE")
FORGOT_PASSWORD_TOKEN_USE_CASE = os.getenv("FORGOT_PASSWORD_TOKEN_USE_CASE")
FORGOT_PASSWORD_SUBJECT = os.getenv("FORGOT_PASSWORD_SUBJECT")


# s3 settings

ENABLE_AWS_S3_BUCKET = bool(int(os.getenv("ENABLE_AWS_S3_BUCKET")))

# this is used for mimicking the aws s3 service into local
ENABLE_MINIO = bool(int(os.getenv("ENABLE_MINIO")))

if ENABLE_AWS_S3_BUCKET:
    DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get("AWS_S3_SECRET_ACCESS_KEY")
    AWS_S3_ACCESS_KEY_ID = os.environ.get("AWS_S3_ACCESS_KEY_ID")
    AWS_DEFAULT_ACL = os.environ.get("AWS_DEFAULT_ACL")
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = os.environ.get("AWS_LOCATION", "media")
    if ENABLE_MINIO:
        AWS_LOCATION = "media"
        AWS_DEFAULT_ACL = None
        AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")

ALL_DAYS = os.environ.get("ALL_DAYS").split(",")
ALL_MONTHS = os.environ.get("ALL_MONTHS").split(",")

ROLE_NAME_PREFIX = r"{}".format(os.environ.get("ROLE_NAME_PREFIX"))
DIVISION_NAME_PREFIX = r"{}".format(os.environ.get("DIVISION_NAME_PREFIX"))

GENERAL_ERROR_MESSAGE = os.environ.get("GENERAL_ERROR_MESSAGE")

# celery settings

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = bool(int(os.getenv("CELERY_TASK_TRACK_STARTED")))

# default threshold

DEFAULT_THRESHOLD_FOR_RECURRING_ACTIVITY_RECORDS = int(
    os.getenv("DEFAULT_THRESHOLD_FOR_RECURRING_ACTIVITY_RECORDS")
)
RE_INVITE_EXPIRATION_TIME = int(os.getenv("RE_INVITE_EXPIRATION_TIME"))

LOWEST_PROGRESS_THRESHOLD = float(os.getenv("LOWEST_PROGRESS_THRESHOLD"))

COMMON_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


from django.db.backends.signals import connection_created


# Set up a listener to connect the logger to the database
def connect_db_logger(sender, connection, **kwargs):
    connection.use_debug_cursor = True


connection_created.connect(connect_db_logger)


ALLOWED_FILE_EXTENSIONS = os.getenv("ALLOWED_FILE_EXTENSIONS").split(",")

ALLOWED_ONE_TIME_RECURRING_ACTIVITY = bool(
    int(os.getenv("ALLOWED_ONE_TIME_RECURRING_ACTIVITY"))
)

SIGN_IN_URL = os.getenv("SIGN_IN_URL")
CEO_ASSISTANT = "ceo-assistant"
CEO = "ceo"


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ALLOWED_HOSTS

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")


# SWAGGER SETTINGS
API_SWAGGER_URL = os.getenv("API_SWAGGER_URL")
SENDGRID_TEMPLATES_FILE_PATH = BASE_DIR.joinpath(
    os.getenv("SENDGRID_TEMPLATES_FILE_NAME")
)

# default language code id german
DEFAULT_GERMAN_LANGUAGE = os.getenv("DEFAULT_GERMAN_LANGUAGE")

# Templates name
INVITE_CEO_TEMPLATE = os.getenv("INVITE_CEO_TEMPLATE")
INVITE_CEO_ASSISTANT_TEMPLATE = os.getenv("INVITE_CEO_ASSISTANT_TEMPLATE")
INVITE_SUCCESS_MANAGER_TEMPLATE = os.getenv("INVITE_SUCCESS_MANAGER_TEMPLATE")
ADD_SUCCESS_MANAGER_TEMPLATE = os.getenv("ADD_SUCCESS_MANAGER_TEMPLATE")
ADD_NEW_USER_TEMPLATE = os.getenv("ADD_NEW_USER_TEMPLATE")
FORGOT_PASSWORD_TEMPLATE = os.getenv("FORGOT_PASSWORD_TEMPLATE")

# # Read JSON data from the file
with open(SENDGRID_TEMPLATES_FILE_PATH, "r") as file:
    SENDGRID_TEMPLATES = json.load(file)

# declared the global attribute logger
GLOBAL_ATTRIBUTE_LOGGER_INSTANCE = AttributeLogger(logger=logging.getLogger(__name__))


# declare lazy exceptions
LAZY_EXCEPTIONS = LazyExceptions().lazy_exceptions
