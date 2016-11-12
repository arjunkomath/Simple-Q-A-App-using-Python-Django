=====================
WELCOME TO DJANGO-QA
=====================
.. image:: https://travis-ci.org/swappsco/django-qa.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/swappsco/django-qa

.. image:: https://coveralls.io/repos/github/swappsco/django-qa/badge.svg?branch=master
   :alt: Coveralls Status
   :target: https://coveralls.io/github/swappsco/django-qa?branch=master

A Simple Q&A App using Python Django
====================================
django-qa_ is a fork from Simple-Q-A-App-using-Python-Django_ aimed to create a pluggable package than allows to implement a StackOverflow-like forum site for your Django web project.
The development of this package is kindly supported by SWAPPS_ and constantly developed by it's colaborators. Feel free to use it, add some issues if you find bugs or think of a really cool feature, even clone it and generate a pull requests to incorporate those cool features made by yourself; If you have special requirements, drop us a few lines_ and perhaps we can help you out too.

.. _django-qa: http://swappsco.github.io/django-qa/
.. _Simple-Q-A-App-using-Python-Django: http://arjunkomath.github.io/Simple-Q-A-App-using-Python-Django
.. _SWAPPS: https://www.swapps.io/
.. _lines: https://www.swapps.io/contact/

Please take in considerations than this application is still under active development and we cannot guarantee that nothing will break between versions. Most of the core features are already there, so we expect to release a beta version soon.

Features
========
* Assumes nothing about the rest of your application.
* Create questions and answers.
* Comment on questions and answers.
* Upvote/Downvote questions and answers.
* Users have a reputation and a profile.
* Support for tagging questions with django-taggit.
* Questions are categorized by latest, popular and most voted.

Installation
============
Django-QA aims at keeping things simple. To install it you have to do what you would do with most django apps.

Install with pip:
.. code-block:: bash
    pip install django-qa

Add to INSTALLED_APPS in your project settings.
.. code-block:: python
    INSTALLED_APPS = (
    ...
    qa,
    ...
    )

Add the package urls to the project:
.. code-block:: python
    urlpatterns = [
        ...,
        url(r'^', include('qa.urls')),
        ...
        ]

Run migrations:
.. code-block:: bash
    python manage.py migrate

And that's it!
