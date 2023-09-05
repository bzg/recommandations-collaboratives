"""
Django settings for urbanvitaliz project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from multisite import SiteID

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "multisite",
    "django.contrib.admin",
    "hijack",
    "hijack.contrib.admin",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "guardian",
    "magicauth",
    "sass_processor",
    "django_vite",
    "markdownx",
    "dbtemplates",
    "tagging",
    "taggit",
    "leaflet",
    "django_gravatar",
    "actstream",
    "notifications",
    "rest_framework",
    "generic_relations",
    "django_filters",
    "csvexport",
    "captcha",
    "ordered_model",
    "dynamic_forms",
    "watson",
    "phonenumber_field",
    "cookie_consent",
    "urbanvitaliz.apps.onboarding",
    "urbanvitaliz.apps.home",
    "urbanvitaliz.apps.projects",
    "urbanvitaliz.apps.tasks",
    "urbanvitaliz.apps.resources",
    "urbanvitaliz.apps.geomatics",
    "urbanvitaliz.apps.addressbook",
    "urbanvitaliz.apps.survey",
    "urbanvitaliz.apps.reminders",
    "urbanvitaliz.apps.communication",
    "urbanvitaliz.apps.invites",
    "urbanvitaliz.apps.crm",
    "urbanvitaliz.apps.training",
]

SITE_ID = SiteID(default=1)

SILENCED_SYSTEM_CHECKS = [
    "sites.E101"  # Check to ensure SITE_ID is an int - ours is an object
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "multisite.middleware.DynamicSiteMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "sesame.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "watson.middleware.SearchContextMiddleware",
    "hijack.middleware.HijackUserMiddleware",
]

ROOT_URLCONF = "urbanvitaliz.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "urbanvitaliz.apps.projects.context_processors.is_switchtender_processor",
                "urbanvitaliz.apps.projects.context_processors.active_project_processor",
            ],
            "loaders": [
                "dbtemplates.loader.Loader",
                "multisite.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "libraries": {
                "common_tags": "urbanvitaliz.templatetags.common_extra",
            },
        },
    },
]

DBTEMPLATES_USE_CODEMIRROR = True

MULTISITE_DEFAULT_TEMPLATE_DIR = "default_site/"

WSGI_APPLICATION = "urbanvitaliz.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "sesame.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# GUARDIAN
GUARDIAN_USER_OBJ_PERMS_MODEL = "home.UserObjectPermissionOnSite"
GUARDIAN_GROUP_OBJ_PERMS_MODEL = "home.GroupObjectPermissionOnSite"

# SESAME Configuration
SESAME_MAX_AGE = 60 * 60 * 24 * 10
SESAME_ONE_TIME = False

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")

STATICFILES_DIRS = [BASE_DIR / "static"]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

# UPLOAD

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
MEDIA_URL = "media/"

SASS_PRECISION = 8

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, "urbanvitaliz/static/css"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Configuration
EMAIL_FROM = "UrbanVitaliz <no-reply@urbanvitaliz.fr>"

# MagicAuth configuration
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "login-redirect"
MAGICAUTH_FROM_EMAIL = EMAIL_FROM
MAGICAUTH_ADAPTER = "urbanvitaliz.apps.home.adapters.UVMagicauthAdapter"
MAGICAUTH_EMAIL_SUBJECT = "Connectez-vous à UrbanVitaliz ici"
MAGICAUTH_EMAIL_FIELD = "email"
MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME = "login-redirect"
MAGICAUTH_TOKEN_DURATION_SECONDS = 60 * 60 * 24 * 3

# MARKDOWNX
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown_link_attr_modifier",
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    "markdown_link_attr_modifier": {
        "new_tab": "on",
        "no_referrer": "external_only",
        "auto_title": "on",
    },
}

# Tagging
FORCE_LOWERCASE_TAGS = True
TAGGIT_CASE_INSENSITIVE = True

# Session Settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60  # 30d * 24h * 60m * 60s

##Cookie consent settings
COOKIE_CONSENT_HTTPONLY = False

# emails to use for notifications
TEAM_EMAILS = ["friches@beta.gouv.fr"]

# BREVO
BREVO_API_KEY = "NO-API-KEY-DEFINED"


# IFrames
X_FRAME_OPTIONS = "SAMEORIGIN"

# RECAPTCHA, V3
RECAPTCHA_REQUIRED_SCORE = 0.85

# DYNAMIC FORMS
DYNAMIC_FORMS_CUSTOM_JS = ""

# ALLAUTH
ACCOUNT_ADAPTER = "urbanvitaliz.apps.home.adapters.UVAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 20
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/login-redirect"

ACCOUNT_FORMS = {
    "login": "urbanvitaliz.apps.home.forms.UVLoginForm",
    "signup": "urbanvitaliz.apps.home.forms.UVSignupForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "urbanvitaliz.apps.home.forms.UVResetPasswordForm",
    "reset_password_from_key": "urbanvitaliz.apps.home.forms.UVResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}

# Django vite
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend/dist"
STATICFILES_DIRS += [DJANGO_VITE_ASSETS_PATH]


# Phonenumbers
PHONENUMBER_DEFAULT_REGION = "FR"

# Hijack
HIJACK_PERMISSION_CHECK = "hijack.permissions.superusers_and_staff"

# eof
