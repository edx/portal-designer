Getting Started
===============
** Note that Portal Designer requires a working edX `devstack <https://github.com/edx/devstack>`_ to function properly **

Initialize and Provision
------------------------
1) Start and provision the edX `devstack <https://github.com/edx/devstack>`_, as portal designer currently relies on devstack
2) Clone the portal designer repo and cd into that directory
3) Run *make dev.provision* to provision a new portal designer environment
4) Run *make dev.init* to start the portal designer app and run migrations

Viewing Designer
------------------------
Once the server is up and running you can view the portal designer at http://localhost:18808/cms

You can login with the username *edx@example.com* and password *edx*

Makefile Commands
--------------------
The `Makefile <../Makefile>`_ includes numerous commands to start the service, but the basic commands are the following:

Start the Docker containers to run the portal designer servers

.. code-block:: bash

    $ make dev.up

Open the shell to the designer container for manual commands

.. code-block:: bash

    $ make app-shell

Open the logs in the designer container

.. code-block:: bash

    $ make designer-logs

Advanced Setup Outside Docker
=============================
The following is provided for informational purposes only. You can likely ignore this section.

Install dependencies
--------------------
Dependencies can be installed via the command below.

.. code-block:: bash

    $ make requirements

Local/Private Settings
----------------------
When developing locally, it may be useful to have settings overrides that you do not wish to commit to the repository.
If you need such overrides, create a file *designer/settings/private.py*. This file's values are
read by `designer/settings/local.py <../designer/settings/local.py>`_, but ignored by Git.

Configure edX OAuth
-------------------
This service relies on the LMS serves as the OAuth 2.0 authentication provider.

Configuring credentials to work with OAuth requires registering a new client with the authentication
provider and updating the Django settings for this project with the client credentials.

A new OAuth 2.0 client can be created at ``http://localhost:18000/admin/oauth2_provider/application/``.
    1. Click the *Add Application* button.
    2. Leave the user field blank.
    3. Specify the name of this service, ``designer``, as the client name.
    4. Set the *URL* to the root path of this service: ``http://localhost:8003/``.
    5. Set the *Redirect URL* to the complete endpoint: ``http://localhost:18808/complete/edx-oauth2/``.
    6. Copy the *Client ID* and *Client Secret* values. They will be used later.
    7. Select *Confidential* as the client type.
    8. Select *Authorization code* as the authorization grant type.
    9. Click *Save*.

Now that you have the client credentials, you can update your settings (ideally in
`designer/settings/local.py <../designer/settings/local.py>`_). The table below describes the relevant settings.

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
