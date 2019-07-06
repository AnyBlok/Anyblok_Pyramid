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

Define views for login and logout. Those views are not automatically applied
to your project.
You must declare the route to use them in the pyramid_load_config method of
your project blok.

First import them in your blok definition __init__.py file:

   from anyblok_pyramid.bloks.auth.views import login, logout

Then set route path in pyramid_load_config method:

   def pyramid_load_config(cls, config):
      config.add_route('login', '/login', request_method='POST')
      config.add_view(view=login, route_name='login', renderer="JSON")
      config.add_route('logout', '/logout', request_method='POST')
      config.add_view(view=logout, route_name='logout')

.. automodule:: anyblok_pyramid.bloks.auth.views
.. autofunction:: login
.. autofunction:: logout

**Configuration**
~~~~~~~~~~~~~~~~~

Define the authentification / authorization policies, This depend on the
options defined in global configuration.

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
