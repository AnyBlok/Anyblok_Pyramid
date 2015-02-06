.. This file is a part of the AnyBlok project
..
..    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

Helper for unittest
===================

For unittest, classes are available to offer some fonctionnalities

.. automodule:: anyblok_pyramid.tests.testcase


PyramidTestCase
---------------

::

    from anyblok_pyramid.tests.testcase import PyramidTestCase

.. autoclass:: PyramidTestCase
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:


PyramidDBTestCase
-----------------

.. warning:: this testcase destroys the test database for each unittest

.. autoclass:: PyramidDBTestCase
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:


PyramidBlokTestCase
-------------------

.. autoclass:: PyramidBlokTestCase
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:
