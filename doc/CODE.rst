.. This file is a part of the AnyBlok / Pyramidproject
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

AnyBlok / Pyramid framework
===========================

AnyBlok / Pyramid controllers
-----------------------------

.. automodule:: anyblok_pyramid.controllers

.. autoexception:: PyramidException
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidMixin
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: Pyramid
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidBase
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidHTTP
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidRPC
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidJsonRPC
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: PyramidXmlRPC
    :show-inheritance:
    :members:
    :noindex:

anyblok_pyramid.workingset
--------------------------

.. automodule:: anyblok_pyramid.workingset

.. autoexception:: WorkingSetException
    :show-inheritance:
    :members:
    :noindex:

.. autoclass:: WorkingSet
    :members:
    :noindex:

anyblok_pyramid.handler
-----------------------

.. automodule:: anyblok_pyramid.handler

.. autoclass:: Handler
    :members:
    :noindex:

.. autoclass:: HandlerHTTP
    :members:
    :noindex:

.. autoclass:: HandlerRPC
    :members:
    :noindex:

anyblok_pyramid.pyramid_config
------------------------------

.. automodule:: anyblok_pyramid.pyramid_config

.. autoclass:: Configurator
    :show-inheritance:
    :members:
    :noindex:

pyramid_config.settings
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyramid_settings
    :noindex:

.. autofunction:: beaker_settings
    :noindex:

pyramid_config.includeme
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyramid_beaker
    :noindex:

.. autofunction:: declare_static
    :noindex:

.. autofunction:: pyramid_config
    :noindex:

.. autofunction:: pyramid_http_config
    :noindex:

.. autofunction:: _pyramid_rpc_config
    :noindex:

.. autofunction:: pyramid_jsonrpc_config
    :noindex:

.. autofunction:: pyramid_xmlrpc_config
    :noindex:

anyblok_pyramid.scripts module
------------------------------

.. automodule:: anyblok_pyramid.scripts

.. autofunction:: anyblok_wsgi
    :noindex:
