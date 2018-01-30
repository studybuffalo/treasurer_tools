Treasurer Tools
===============
A Django-based system to assist Non-Profit Organization treasurers in managing/tracking finances

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with help from Cookiecutter Django

:License: GPLv3

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Deployment
----------

The following details how to deploy this application.

Issues to Workout
-----------------

- Developer/Superuser
- Branch Delegate(s)
- President
  - President only one with ability to upgrade user status?
- Treasurer
