# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            }
        }

TIME_ZONE = 'America/Chicago'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'


SECRET_KEY = 'l#^#iad$8$4=dlh74$!xs=3g4jb(&j+y6*ozy&8k1-&d+vruzy'

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        )

ROOT_URLCONF = 'qa.urls'

INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django_markdown',
        'taggit',
        'qa',
        'hitcount',

        )

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [],
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/foo/list/'

QA_SETTINGS = {
    'qa_messages': True,
    'qa_description_optional': False,
    'count_hits': True,
    'reputation': {
        'CREATE_QUESTION': 0,
        'CREATE_ANSWER': 0,
        'CREATE_ANSWER_COMMENT': 0,
        'CREATE_QUESTION_COMMENT': 0,
        'ACCEPT_ANSWER': 0,
        'UPVOTE_QUESTION': 0,
        'UPVOTE_ANSWER': 0,
        'DOWNVOTE_QUESTION': 0,
        'DOWNVOTE_ANSWER': 0,
    }
}
