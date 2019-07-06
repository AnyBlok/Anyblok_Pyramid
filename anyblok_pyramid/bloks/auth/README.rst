.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This blok define a **User** model and add the basics of Pyramid Authentication
and Authorization policy.
It is required by the 'password' and 'authorization' bloks.
Used alone it adds : 

* **User** and **User.Role** models
* **login** / **logout** extendable views (That will throw an exception until
  you require 'password' and 'authorization' bloks into your project.)

Basically you can:

* Create a new user::

      user = registry.User.insert(
          login='jssuzanne',
          first_name='Jean-Sébastien',
          last_name='Suzanne'
      )

      user.name  # Jean-Sébastien SUZANNE

* Add a role to the created user::

      role = registry.User.Role.insert(
          name='admin',
          label='Administrator'
      )
      user.roles.append(role)

      user.roles # [<Model.User.Role(children=[], label='Administrator', name='admin', parents=<not loaded>, users=<Model.User len(1)>)>]
      role.users # [<Model.User(first_name='Jean-Sébastien', last_name='Suzanne', login='jssuzanne', roles=<Model.User.Role len(1)>)>]

* Check a permission for a user to use a resource::

      from anyblok_pyramid.security import AnyBlokResourceFactory

      @view_config(
          route_name='my_view',
          factory=AnyBlokResourceFactory('my_resource')
          permission='my_permission'
      )
      def my_view(request):
          return Response('Ok I have the permission')


.. warning::

    Remember that until you had credential behaviours, the 'login' view from
    'auth.views' will raise an 'HTTPUnauthorized' exception.
