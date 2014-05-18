LMMS Sharing Platform 2
========================

Code for new Django-based LMMS Sharing Platform.

License: GPLv2 or later


Usage
=====

Initializing local database:

    ./manage.py syncdb


Run web server:

    ./manage.py runserver


For testing purposes, fill database with pseudo-data by running

    ./manage.py loadtestdata backend.<Model>:<n>


Requirements
============

This project uses the following third party django apps:

* [django-allauth]
* [django-autofixture][] (Only for testing purposes)

Install them via

    pip install -r requirements.txt

[django-allauth]: https://github.com/pennersr/django-allauth
[django-autofixture]: https://github.com/gregmuellegger/django-autofixture


