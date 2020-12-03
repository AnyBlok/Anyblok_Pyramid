.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
..    Copyright (C) 2020 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
..    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

CHANGELOG
=========

1.2.0 (2020-12-03)
------------------

* Added **restrict_query_by_user** decorator in order to apply query filters
  related to a given user
* Added utilities to setup roles and authorizations

1.1.1 (2020-10-16)
------------------

* Fixed the size of the fields **model**, because they have a
  foreign key to the model  **Model.System.Model** on the field
  **name**. The next version of AnyBlok check that the size are the same

1.1.0 (2020-08-31)
------------------

* Added IODC by Pierre Verkest <pierreverkest84@gmail.com>
* Added enum_adapter for enum Column
* Allow to set HttpOnly cookie in pyramid authkt configuration

1.0.0 (2020-05-12)
------------------

* Added **pyramid** blok, used to do a better isolation
* Created a new adapter for timedelta objects. It can parametrized using
  the new timedelta_adapter_factory and TimedeltaModes enumeration
* Removed **Python 3.4** capability
* Removed **Python 3.5** capability
* Refactored unittest, replaced nose by pytest

0.9.5 (2019-11-01)
------------------

* Fixed, missing dependencies

0.9.4 (2019-11-01)
------------------

* Fixed #21 that `zope.sqlalchemy 1.2 <https://pypi.org/project/zope.sqlalchemy/#id1>`_ rename a class
* [ADD] **user-identity** blok. Splitted anyblok_pyramid/auth blok to 
  separate authentication fields from user identity fields

0.9.3 (2019-06-23)
------------------

* Refactored unittest and helpper from nose to pytest


0.9.2 (2018-08-10)
------------------

* Fix get_acl method
* Add max age for static path, issue #13

0.9.1 (2018-05-30)
------------------

* Fix get_acl method
* Update logging output

0.9.0 (2018-02-27)
------------------

* [FIX] commited session with pyramid
* [ADD] Authentication configuration
* [ADD] **auth** blok
* [ADD] **auth-password** blok
* [ADD] **authorization** blok
* [FIX] console script whith gunicorn and wsgi server
  Put all the serveur in loadwithoutmigration=True, AnyBlok can add some
  lock during the migration and must do in specal action

0.8.2 (2017-12-23)
------------------

* [FIX] anyblok cache invalidation
* [FIX] replace SQLAlchemy deprecated extension by session events

0.8.1 (2017-11-28)
------------------

* [REF] replace the overload of ``init_registry`` by ``init_registry_with_bloks``

0.8.0 (2017-10-14)
------------------

* [DEL] Remove configuration group definition ``preload``
* [REF] use ``configuration_post_load`` function to initialize services

0.7.2 (2017-10-18)
------------------

* [ADD] Some apdater to convert to json

  - datetime_adapter
  - date_adapter
  - decimal_adapter
  - uuid_adapter
  - bytes_adapter

0.7.1 (2016-12-05)
------------------

* [FIX] add pluggins in autoload configuration for unittest
* [FIX] type replace asset by assert
* [FIX] fix gunicorn script, load the plugins config part

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
