Treasurer Tools
===============

A Django-based system to assist Non-Profit Organization treasurers in managing/tracking finances.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: GPLv3

Basic Commands
--------------
Initialize Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Install the development environment with Poetry::

    $ poetry install

2. Copy the ``/config/settings/.treasurer_tools.env`` file to
   ``/config/settings/treasurer_tools.env`` and update the details for
   your environment.
3. Run the database migrations::

    $ poetry run python manage.py migrate

4. Load the Country data::

   $ poetry run python manage.py loaddata country.json

Running The Test Server
^^^^^^^^^^^^^^^^^^^^^^^
1. Run the following command::

    $ poetry run python manage.py runserver

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests::

    $ poetry run pytest

Issues to Workout
-----------------

- Developer/Superuser
- Branch Delegate(s)
- President
  - President only one with ability to upgrade user status?
- Treasurer
