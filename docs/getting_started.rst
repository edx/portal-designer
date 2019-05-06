Getting Started
===============

** Requires a working edx devstack to function properly **

1) Run `make dev.provision` to provision a new environment.
2) Run `make dev.init` to start the app and run migrations


Install dependencies
--------------------
Dependencies can be installed via the command below.

.. code-block:: bash

    $ make requirements


Local/Private Settings
----------------------
When developing locally, it may be useful to have settings overrides that you do not wish to commit to the repository.
If you need such overrides, create a file :file:`portal_designer/settings/private.py`. This file's values are
read by :file:`portal_designer/settings/local.py`, but ignored by Git.


Configure edX OAuth
-------------------
This service relies on the LMS serves as the OAuth 2.0 authentication provider.

Configuring credentials to work with OAuth requires registering a new client with the authentication
provider and updating the Django settings for this project with the client credentials.

A new OAuth 2.0 client can be created at ``http://localhost:18000/admin/oauth2_provider/application/``.
    1. Click the :guilabel:`Add Application` button.
    2. Leave the user field blank.
    3. Specify the name of this service, ``portal_designer``, as the client name.
    4. Set the :guilabel:`URL` to the root path of this service: ``http://localhost:8003/``.
    5. Set the :guilabel:`Redirect URL` to the complete endpoint: ``http://localhost:18808/complete/edx-oauth2/``.
    6. Copy the :guilabel:`Client ID` and :guilabel:`Client Secret` values. They will be used later.
    7. Select :guilabel:`Confidential` as the client type.
    8. Select :guilabel:`Authorization code` as the authorization grant type.
    9. Click :guilabel:`Save`.

Now that you have the client credentials, you can update your settings (ideally in
:file:`portal_designer/settings/local.py`). The table below describes the relevant settings.

+-----------------------------------+----------------------------------+--------------------------------------------------------------------------+
| Setting                           | Description                      | Value                                                                    |
+===================================+==================================+==========================================================================+
| SOCIAL_AUTH_EDX_OAUTH2_KEY        | OAuth 2.0 client key             | (This should be set to the value generated when the client was created.) |
+-----------------------------------+----------------------------------+--------------------------------------------------------------------------+
| SOCIAL_AUTH_EDX_OAUTH2_SECRET     | OAuth 2.0 client secret          | (This should be set to the value generated when the client was created.) |
+-----------------------------------+----------------------------------+--------------------------------------------------------------------------+
| SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT   | OAuth 2.0 authentication URL     | http://127.0.0.1:18000/oauth2                                            |
+-----------------------------------+----------------------------------+--------------------------------------------------------------------------+

Run migrations
--------------
Local installations use SQLite by default. If you choose to use another database backend, make sure you have updated
your settings and created the database (if necessary). Migrations can be run with `Django's migrate command`_.

.. code-block:: bash

    $ python manage.py migrate

.. _Django's migrate command: https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-migrate


Run the server
--------------
The server can be run with `Django's runserver command`_. If you opt to run on a different port, make sure you update
OAuth2 client via LMS admin.

.. code-block:: bash

    $ python manage.py runserver 8003

.. _Django's runserver command: https://docs.djangoproject.com/en/1.11/ref/django-admin/#runserver-port-or-address-port
