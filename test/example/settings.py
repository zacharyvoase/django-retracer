# -*- coding: utf-8 -*-

import os.path as p
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = p.dirname(p.abspath(__file__))

sys.path.append(p.join(p.dirname(p.dirname(PROJECT_ROOT)), 'src'))

ADMINS = (
    ('Zachary Voase', 'zacharyvoase@me.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = p.join(PROJECT_ROOT, 'dev.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e5!mk_i2!z_w=^a2$-rlz+9jm)iom7!@+=2z@_@hkfze0zv$=v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djretr.middleware.RetracerMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'djretr',
    'example.feedback',
)

ATTENTION_REQUEST_ATTR = 'attn'
ATTENTION_SESSION_KEY = '_attn'