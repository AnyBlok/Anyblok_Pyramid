.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

CHANGELOG
=========

Future
------

.. warning::

    this version can be uncapable with the previous version

.. note::

    Works only with AnyBlok 0.5.0 and after

* [REF] Add entry point to add new pyramid includeme and settings
* [DEL] properties decorator, it is useless because pyramid have a better
  behaviour
* [REF] add workingset to define overwritable callback used for application,
  no for the blok, add first callback, get_registry
* [REF] unit test cause of new version of AnyBlok 0.5.0

0.3.2
-----

* [REF] cause of upgrade version of AnyBlok 0.4.0

0.3.1
-----

* [FIX] default value for beaker, None is better than ''

0.3.0
-----

* [IMP] console script argsparse for pyramid and beaker
* [ADD] MANIFEST.in
* [FIX] script cause of remove logging configuration from AnyBlok

0.2.0
-----

* [ADD] configurator callable
* [REF] Adapt the import of python module of the blok, cause of the change in
  AnyBlok version 0.2.2


0.1.0
-----

Main version of AnyBlok / Pyramid. You can with this version

* Declare Views / Routes for application
* Declare controller (Views / Routes) which depend of the installation of bloks
    * XHR
    * JsonRPC
    * XmlRPC
* Possibility to check some property as authentification
* Possibility to define properties check
