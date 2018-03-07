.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

**User**
~~~~~~~~

.. automodule:: anyblok_pyramid.bloks.auth.user

.. autoanyblok-declaration:: User                                                     
    :members:                                                                   
    :undoc-members:                                                             
    :show-inheritance:
    :noindex:

**Role**
~~~~~~~~

.. automodule:: anyblok_pyramid.bloks.auth.role

.. autoanyblok-declaration:: Role                                                     
    :members:                                                                   
    :undoc-members:                                                             
    :show-inheritance:
    :noindex:


**Views**
~~~~~~~~~

Give the views forlogin and logout, this views, is not applied by default
You must declare the route to use them

.. automodule:: anyblok_pyramid.bloks.auth.views
.. autofunction:: login
.. autofunction:: logout

**Configuration**
~~~~~~~~~~~~~~~~~

Define the authentification / authorization policies, This depend of the options
passed on the global configuration

.. automodule:: anyblok_pyramid.bloks.auth.pyramid
.. autofunction:: getAuthenticationPolicy
.. autofunction:: getAuthTktAuthenticationPolicy
.. autofunction:: getRemoteUserAuthenticationPolicy
.. autofunction:: getSessionAuthenticationPolicy
.. autofunction:: getBasicAuthAuthenticationPolicy

**Exceptions**
~~~~~~~~~~~~~~

.. automodule:: anyblok_pyramid.bloks.auth.exceptions
.. autoexception:: RecursionRoleError
