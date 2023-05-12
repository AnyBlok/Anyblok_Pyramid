.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

How to use it
~~~~~~~~~~~~~

This Blok add **Pyramid.CredentialStore** model, a simple login / password table.
You can not add credential for an **unexisting user** because one foreign key
constraint is defined between both.

* Before all you must create a new user::

      user = registry.Pyramid.User.insert(login='jssuzanne')

* Then define a credential for this user::

      user_credential = registry.Pyramid.CredentialStore.insert(
          login=user.login,
          password='secret password',
      )


* At this point you can check if a given password is the good one::

      user_credential.password == "not the good one" # False
      user_credential.password == "secret password" # True

* You can also use 'registry.Pyramid.User.check_login' method to check that a password
  and a login match::

      registry.Pyramid.User.check_login(login='jssuzanne', password='a bad one') # Will raise an HTTPUnauthorized exception
      registry.Pyramid.User.check_login(login='jssuzanne', password='secret password') # 'jssuzanne'


.. note::

    The password use the **Password** column, the value is an encrypted string
    in database and can not be revealed during the execution of the application,
    you can only compare it.
