.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This blok helps defining authorization for **User or Role** on a **resource or
model**.

* Create an user::

      user = registry.Pyramid.User.insert(login='jssuzanne')

* Add an authorization for the user to access a Pyramid resource::

      registry.Pyramid.Authorization.insert(
          resource='something',
          user=user,
          perm_create=dict(matched=True),
          perm_read=dict(matched=True),
          perm_update=dict(matched=True),
          perm_delete=dict(matched=True)
      )

      registry.Pyramid.Authorization.get_acl('jssuzanne', 'something')
      #  [
      #      (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
      #      (Deny, 'jssuzanne', ALL_PERMISSIONS),
      #  ]

* An user can have roles, this way you can define an authorization for a role
  and all users that have this role will be authorized::

      role = registry.Pyramid.Role.insert(
          name='admin',
          label='Administrator'
      )
      user.roles.append(role)

      registry.Pyramid.Authorization.insert(
          resource='otherthing',
          role=role,
          perm_create=dict(matched=True),
          perm_read=dict(matched=True),
          perm_update=dict(matched=True),
          perm_delete=dict(matched=True)
      )

      registry.Pyramid.Authorization.get_acl('jssuzanne', 'otherthing')
      #  [
      #      (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
      #      (Deny, 'jssuzanne', ALL_PERMISSIONS),
      #  ]


The permission is stored in a **Json** column, the permissions can be CRUD
or any other one that is defined.

Each permission can defined three keys:

* condition: ``Query.filter_condition``, if it's empty then the condition is marked as True
* matched: If condition is True, the entry indicate the value (default None)
* unmatched: If condition is False, the entry indicate the value (default None)

``matched`` and ``unmatched`` can have three values:

* True: Add the permission in **Allow** list,
* False: Add the permission in the **Deny** list,
* None: Do nothing, because this rule can not **Allow** or **Deny**
