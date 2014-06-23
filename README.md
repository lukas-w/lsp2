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

    ./manage.py loadtestdata submissions.<Model>:<n>


Requirements
============

This project uses the following python packages:

* For production
    * [Django] 1.7
    * [django-allauth]
    * [django-model-utils]
    * [markdown]
    * [django-markupfield] (Currently broken)
* For testing/development
    * [django-autofixture][] (Only for testing purposes)
* For the import script
    * [PyMySQL]
    * [ftfy]

Install them via

```sh
    $ pip install -r requirements.txt
    $ pip install -r requirements.dev.txt
    $ pip install -r requirements.import.txt
```

respectively.

[django]: https://www.djangoproject.com/
[django-allauth]: https://github.com/pennersr/django-allauth
[django-model-utils]: https://github.com/carljm/django-model-utils/
[markdown]: https://pypi.python.org/pypi/Markdown]
[django-markupfield]: https://github.com/jamesturk/django-markupfield

[django-autofixture]: https://github.com/gregmuellegger/django-autofixture

[PyMySQL]: http://www.pymysql.org/
[ftfy]: https://github.com/LuminosoInsight/python-ftfy
