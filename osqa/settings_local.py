# encoding:utf-8
import os
import urlparse
import sys
import os.path

SITE_SRC_ROOT = os.path.dirname(__file__)
LOG_FILENAME = 'django.osqa.log'

#for logging
import logging
logging.basicConfig(
    filename=os.path.join(SITE_SRC_ROOT, 'log', LOG_FILENAME),
    level=logging.ERROR,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

#ADMINS and MANAGERS
ADMINS = (
        ('Jan Backes', 'jan@blackpixels.com'),
        ('Manuel Holtz', 'manuel@blackpixels.com'),
        )
MANAGERS = ADMINS

DEBUG = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True
}
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')


if 'PROD' in os.environ:
    try:
        # Check to make sure DATABASES is set in settings.py file.
        # If not default to {}
        if 'DATABASES' not in locals():
            DATABASES = {}

        if 'DATABASE_URL' in os.environ:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])

            # Ensure default database exists.
            DATABASES['default'] = DATABASES.get('default', {})

            # Update with environment configuration.
            DATABASES['default'].update({'NAME': url.path[1:],
                                         'USER': url.username,
                                         'PASSWORD': url.password,
                                         'HOST': url.hostname,
                                         'PORT': url.port,})
            if url.scheme == 'postgres':
                DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


    except Exception:
            print 'Unexpected error:', sys.exc_info()
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'paleo_db',
            'USER': 'paleodiet',
            'PASSWORD': 'gb0fCiGciIe0',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


CACHE_BACKEND = 'file://%s' % os.path.join(os.path.dirname(__file__),'cache').replace('\\','/')
#CACHE_BACKEND = 'dummy://'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# This should be equal to your domain name, plus the web application context.
# This shouldn't be followed by a trailing slash.
# I.e., http://www.yoursite.com or http://www.hostedsite.com/yourhostapp
APP_URL = 'http://paleodiet.herokuapp.com'

#LOCALIZATIONS
TIME_ZONE = 'Europe/Berlin'

#OTHER SETTINGS

USE_I18N = True
LANGUAGE_CODE = 'de'

LOCALE_PATHS = (
    'osqa/locale/',
    'locale',
)

DJANGO_VERSION = 1.1
OSQA_DEFAULT_SKIN = 'nuxeo'

DISABLED_MODULES = ['books', 'recaptcha', 'project_badges', 'sphinxfulltext', 'pgfulltext']

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2',
}
