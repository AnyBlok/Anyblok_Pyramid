.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This Blok define credential from an **existing user**. You can not add credential
for an **unexisting user** because one foreign key constraint is defined between both.

* You must have an user::

      user = registry.User.insert(
          login='jssuzanne',
          first_name='Jean-Sébastien',
          last_name='Suzanne'
      )

* Define the credential::
      
      registry.User.CredentialStore.insert(
          login=user.login,
          password='secret password',
      )

.. note::
    
    The password use the **Password** column, the value is crypted is table and can not be
    get during the execution of the application, You only compare it
