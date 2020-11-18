.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://img.shields.io/pypi/pyversions/anyblok_delivery.svg?longCache=True
    :alt: Python versions

.. image:: https://travis-ci.org/AnyBlok/Anyblok_Pyramid.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/Anyblok_Pyramid
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/Anyblok_Pyramid/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/Anyblok_Pyramid?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/Anyblok_Pyramid.svg
   :target: https://pypi.python.org/pypi/Anyblok_Pyramid/
   :alt: Version status
         
.. image:: https://readthedocs.org/projects/anyblok-pyramid/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://doc.anyblok-pyramid.anyblok.org/en/latest/?badge=latest


AnyBlok / Pyramid
=================

AnyBlok / Pyramid make the link between `AnyBlok <http://doc.anyblok.org>`_ and
`Pyramid <http://pyramid.readthedocs.org/>`_

It also gives you some bloks for adding user http authentication and role
based authorization to your project.


+-------------------+--------------+----------------------------------------------------------+
| Blok              | Dependencies | Description                                              |
+===================+==============+==========================================================+
| **Pyramid**       |              | Add hooks to connect Pyramid authentification, OIDC      |
|                   |              | Relying Party and authorization                          |
+-------------------+--------------+----------------------------------------------------------+
| **auth**          | **pyramid**  | Add 'User' and 'User.Role' models.                       |
+-------------------+--------------+----------------------------------------------------------+
| **auth-password** | **auth**     | Add 'User.CredentialStore' model, a simple               |
|                   |              | login, password table                                    |
+-------------------+--------------+----------------------------------------------------------+
| **authorization** | **auth**     | Add 'User.Authorization' model for managing permissions  |
+-------------------+--------------+----------------------------------------------------------+

AnyBlok / Pyramid is released under the terms of the `Mozilla Public License`.

See the `latest documentation <http://doc.anyblok-pyramid.anyblok.org/>`_
