.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This blok defined **User** and the base of the Authentication / Authorization.

Alone this Blok is useless because no credential and autorization are defined

You can:

* Create an user::

      user = registry.User.insert(
          login='jssuzanne',
          first_name='Jean-Sébastien',
          last_name='Suzanne'
      )

      user.name  # Jean-Sébastien SUZANNE

* Add a role at this user::

      role = registry.User.Role.insert(
          name='admin',
          label='Administrator'
      )
      user.roles.append(role)

* check a permission for a user to use a resource::

      from anyblok_pyramid.security import AnyBlokResourceFactory

      @view_config(
          route_name='my_view',
          factory=AnyBlokResourceFactory('my_resource')
          permission='my_permission'
      )
      def my_view(request):
          return Response('Ok I have the permission')


.. warning::

    The have to define credential behaviours, to login and logout
