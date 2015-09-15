"""
Django settings for mdid3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

# install_dir = os.path.dirname(os.path.dirname(__file__))

# MDID repo root
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
# setting for django-extensions
BASE_DIR = PROJECT_ROOT
# the rooibos directory
CONTRIB_DIR = os.path.join(PROJECT_ROOT, 'rooibos', 'contrib')
ROOIBOS_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'rooibos'))

if not BASE_DIR in sys.path: sys.path.append(BASE_DIR)
if not CONTRIB_DIR in sys.path: sys.path.append(CONTRIB_DIR)

# STATIC_FILES
# STATIC_ROOT: The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    #  these files will be copied up by collectstatic
    os.path.normpath(os.path.join(ROOIBOS_ROOT, 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

# TODO: find references to STATIC_DIR and change to STATIC_ROOT
# TODO: why? STATIC_DIR over STATIC_ROOT? why?
STATIC_DIR = STATIC_ROOT

COMPRESS_OUTPUT_DIR = 'CACHE'

FAVICON_URL = os.path.normpath(os.path.join(STATIC_URL, 'images', 'favicon.ico'))

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

USE_ETAGS = False

# When set to True, may cause problems with basket functionality
SESSION_SAVE_EVERY_REQUEST = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'change me in settings_local.py'


# MDID3 specific settings

# Settings that should be available in template rendering
EXPOSE_TO_CONTEXT = (
    'STATIC_DIR',
    'STATIC_ROOT',
    'PRIMARY_COLOR',
    'SECONDARY_COLOR',
    'CUSTOM_TRACKER_HTML',
    'ADMINS',
    'LOGO_URL',
    'FAVICON_URL',
    'COPYRIGHT',
    'TITLE',
    'SHOW_FRONTPAGE_LOGIN',
    'MASTER_TEMPLATE',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.humanize',
    # 'django.contrib.comments' removed from django in 1.7
    'django_comments',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_extensions',
    'rooibos',
    'rooibos.data',
    'rooibos.migration',
    'rooibos.util',
    'rooibos.access',
    'rooibos.solr',
    'rooibos.storage',
    'rooibos.legacy',
    'rooibos.ui',
    'rooibos.viewers',
    'rooibos.help',
    'rooibos.presentation',
    'rooibos.statistics',
    'rooibos.federatedsearch',
	'rooibos.unitedsearch',
    #'rooibos.federatedsearch.artstor',
    #'rooibos.federatedsearch.flickr',
    'rooibos.converters',
    'rest_framework',
    # replace rooibos.contrib.tagging with django-tagging
    'tagging',
    'rooibos.workers',
    'rooibos.userprofile',
    'rooibos.mediaviewer',
    'rooibos.megazine',
    'rooibos.groupmanager',
    'rooibos.pdfviewer',
    'rooibos.pptexport',
    'rooibos.audiotextsync',
    # TODO: clear rooibos.contrib of apps that can be installed as a normal dependency via requirements.txt
    #'rooibos.contrib.google_analytics',
    'rooibos.contrib.pagination',
    'rooibos.contrib.impersonate',
    'compressor',
    'debug_toolbar',
)

TEMPLATE_LOADERS = (
    (
		'django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # "django.core.context_processors.",
    "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "rooibos.context_processors.settings",
    "rooibos.context_processors.selected_records",
    "rooibos.context_processors.current_presentation",
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'rooibos.middleware.Middleware',
    'rooibos.sslredirect.SSLRedirect',
    'rooibos.ui.middleware.PageTitles',
    'django.middleware.common.CommonMiddleware',
    'rooibos.util.stats_middleware.StatsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'rooibos.api.middleware.CookielessSessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'rooibos.contrib.pagination.middleware.PaginationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'rooibos.storage.middleware.StorageOnStart',
    'rooibos.access.middleware.AccessOnStart',
    'rooibos.data.middleware.DataOnStart',
    'rooibos.middleware.HistoryMiddleware',
    'rooibos.access.middleware.AnonymousIpGroupMembershipMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'rooibos.help.middleware.PageHelp',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STORAGE_SYSTEMS = {
    'local': 'rooibos.storage.localfs.LocalFileSystemStorageSystem',
    'online': 'rooibos.storage.online.OnlineStorageSystem',
    'pseudostreaming': 'rooibos.storage.pesudostreaming.PseudoStreamingStorageSystem',
    'cloudfiles': 'rooibos.storage.cloudfiles.CloudFilesStorageSystem',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'rooibos.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

WEBSERVICE_NAMESPACE = "http://www.jmu.edu/webservices"

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Methods to be called after a user is successfully authenticated
# using an external backend (LDAP, IMAP, POP).
# Must take two parameters:
#   user object
#   dict of string->list/tuple pairs (may be None or empty)
# Returns:
#   True: login continues
#   False: login rejected, try additional login backends if available
LOGIN_CHECKS = (
    'rooibos.access.models.update_membership_by_attributes',
)

# move to settings_local for system customization
TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(ROOIBOS_ROOT, 'templates')),
	os.path.normpath(os.path.join(ROOIBOS_ROOT, 'unitedsearch', 'templates'))
#     os.path.normpath(os.path.join(ROOIBOS_ROOT, 'access', 'templates')),
#     os.path.normpath(os.path.join(ROOIBOS_ROOT, 'ui', 'templates')),
#     os.path.normpath(os.path.join(ROOIBOS_ROOT, 'contrib', 'google_analytics', 'templates')),
 )

PDF_PAGESIZE = 'letter'  # 'A4'

SHOW_FRONTPAGE_LOGIN = "yes"

MASTER_TEMPLATE = 'master_root.html'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


GROUP_MANAGERS = {
    #   'nasaimageexchange': 'rooibos.federatedsearch.nasa.nix.NasaImageExchange',
}

## these should be overridden by settings_local

FLICKR_KEY = '3a092eb0151a289f86ea4b9bd71c3d8e'
FLICKR_SECRET = 'a90b7a165091cab4'

additional_settings = [
    'settings_local',
]

## various app settings

# required for contrib.tagging
FORCE_LOWERCASE_TAGS = False

additional_settings.extend(filter(None, os.environ.get('ROOIBOS_ADDITIONAL_SETTINGS', '').split(';')))

# Load settings for additional applications

while additional_settings:
    settings = additional_settings.pop(0)
    module = __import__(settings, globals(), locals(), 'rooibos')
    for setting in dir(module):
        if setting == setting.upper():
            if locals().has_key(setting):
                if isinstance(locals()[setting], dict):
                    locals()[setting].update(getattr(module, setting))
                elif isinstance(locals()[setting], tuple):
                    locals()[setting] += (getattr(module, setting))
                else:
                    locals()[setting] = getattr(module, setting)
            else:
                locals()[setting] = getattr(module, setting)
        elif setting == 'additional_settings':
            additional_settings[:0] = getattr(module, setting)
        elif setting == 'remove_settings':
            for remove_setting in getattr(module, setting):
                del locals()[remove_setting]
