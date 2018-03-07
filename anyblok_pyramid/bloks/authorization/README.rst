.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This blok defined authorization for **User or Role** on a **resource or model**.

* Create an user::

      user = registry.User.insert(
          login='jssuzanne',
          first_name='Jean-Sébastien',
          last_name='Suzanne'
      )

      user.name  # Jean-Sébastien SUZANNE

* Add an autorization::

      user.roles.append(role)
      registry.User.Authorization.insert(
          resource='something',
          user=user,
          perm_create=dict(matched=True),
          perm_read=dict(matched=True),
          perm_update=dict(matched=True),
          perm_delete=dict(matched=True)
      )

      registry.User.Authorization.get_acl('jssuzanne', 'something')
      #  [
      #      (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
      #      (Deny, 'jssuzanne', ALL_PERMISSIONS),
      #  ]


The permissiosn is stored in the **Json** column, the permission can be the CRUD and also
any another permission.

Each permission can defined three keys:

* condition: ``Query.filter_condition``, if the empty then the condition is marked as True
* matched: If condition is True, the entry indicate the value (default None)
* unmatched: If condition is False, the entry indicate the value (default None)

``matched`` and ``unmatched`` can have three values:

* True: Add the permission in **Allow** list,
* False: Add the permission in the **Deny** list,
* None: Do nothing, because this rule can not **Allow** or **Deny**
