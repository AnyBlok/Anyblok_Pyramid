.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

CHANGELOG
=========

0.7.0 (2016-07-11)
------------------

* [FIX] Adapte for new release of AnyBlok 0.9.0
* [Add] Plugin get_db_name
* [ADD] some unittest
* [REF] Update doc

0.6.3 (2016-06-20)
------------------

* [FIX] bad release for 0.6.2

0.6.2 (2016-06-20)
------------------

* [FIX] utf-8 encoding in setup, need for readthedocs
* [REF] move from bitbucket (mercurial) to github (git)

0.6.1 (2016-04-18)
------------------

* [FIX] for Python < 3.5

0.6.0 (2016-04-18)
------------------

.. warning::

    This version break the compatibility with previous version. The goal
    is to use all the functionnality of pyramid, and give the tools to make
    the bind with AnyBlok easily

* [REM] remove old Controller declarations:
   * Declarations.Pyramid
   * Declarations.PyramidHTTP
   * Declarations.PyramidJSONRPC
   * Declarations.PyramidXMLRPC
* [ADD] add anyblok request property
  ::

      registry = request.anyblok.registry

* [ADD] installed_blok predicate for route and view
  ::

      @view_config(route_name='hello', installed_blok='my-blok')
      def say_hello(request):
          ...

* [ADD] need_anyblok_registry predicate for route and view
  ::

      @view_config(route_name='hello', need_anyblok_registry=True)
      def say_hello(request):
          ...


0.5.3 (2016-03-17)
------------------

* [REF] Preload database, add log and check if the database exist before load
  it
* [FIX] catch simple exception to reput in real rpc exception

0.5.2 (2016-01-15)
------------------

* [FIX] use anyblok parser for config with gunicorn
* [REF] entry point init is now in anyblok

0.5.1 (2016-01-08)
------------------

* [REF] Adapt with the new version of AnyBlok
* [IMP] Add new entry point to load function before load AnyBlok bloks

0.5.0 (2016-01-07)
------------------

* [ADD] pyramid_pm and zope.sqlalchemy to isolate each controller call

0.4.1 (2015-10-9)
-----------------

* [ADD] console script, implementation with gunicorn only
* [ADD] wsgi script to give un app for wsgi server

0.4.0 (2015-08-25)
------------------

.. warning::

    this version can not be capable with the previous version

.. note::

    Works only with AnyBlok 0.5.1 and after

* [REF] Add entry point to add new pyramid includeme and settings
* [DEL] properties decorator, it is useless because pyramid have a better
  behaviour
* [REF] add workingset to define overwritable callback used for application,
  no for the blok, add first callback, get_registry
* [REF] unit test cause of new version of AnyBlok 0.5.0
* [FIX] unit test case, update controller to unload the declaration when
  BlokManager are unloaded

0.3.2 (2015-06-22)
------------------

* [REF] cause of upgrade version of AnyBlok 0.4.0

0.3.1 (2015-05-04)
------------------

* [FIX] default value for beaker, None is better than ''

0.3.0 (2015-05-04)
------------------

* [IMP] console script argsparse for pyramid and beaker
* [ADD] MANIFEST.in
* [FIX] script cause of remove logging configuration from AnyBlok

0.2.0 (2015-03-15)
------------------

* [ADD] configurator callable
* [REF] Adapt the import of python module of the blok, cause of the change in
  AnyBlok version 0.2.2


0.1.0 (2015-02-07)
------------------

Main version of AnyBlok / Pyramid. You can with this version

* Declare Views / Routes for application
* Declare controller (Views / Routes) which depend of the installation of bloks
    * XHR
    * JsonRPC
    * XmlRPC
* Possibility to check some property as authentification
* Possibility to define properties check
