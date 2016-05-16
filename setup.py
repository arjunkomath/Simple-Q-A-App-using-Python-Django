#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='django-qa',
    version='0.0.21',
    description='Pluggable django app for Q&A',
    long_description=long_description,
    author='arjunkomath, cdvv7788, sebastian-code, jlariza, swappsco',
    author_email='dev@swapps.co',
    url='https://github.com/swappsco/django-qa',
    license='MIT',

    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    install_requires=[
        'django-annoying',
        'django_bootstrap3',
        'django_markdown',
        'pillow',
        'django-taggit',
        'pytz==2015.6'
    ],
    extras_require={
        'i18n': [
            'django-modeltranslation>=0.5b1',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
