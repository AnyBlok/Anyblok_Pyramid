.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

MEMENTO
=======

Anyblok / Pyramid mainly depends on:

* Python 3.2+
* `AnyBlok <http://doc.anyblok.org>`_
* `Pyramid <http://pyramid.readthedocs.org>`_

If the scrip ``anyblok_wsgi`` is used to start the ``WSGI`` application,
the you can not declare ``route`` and ``view``. AnyBlok / Pyramid define two
familly of controller:

* Controller which no depend of blok
* Controller which depend of the installation or not of bloks

Pyramid ``route`` and ``view`` which does not depend of the bloks
-----------------------------------------------------------------

The goal is to declare in your application code source the ``route`` and the
``view``::

    from anyblok import Declarations
    Pyramid = Declarations.Pyramid

Declare a ``view``::

    @Pyramid.add_view('route name')
    def myview(request):
        ...

.. note::

    The decorator ``add_view`` is just a wrapper of `add_view
    <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
    config.html#pyramid.config.Configurator.add_view>`_

    the args already filled by the wraper are:

    * view: is the decorated function
    * name: is the **route name**

Declare a ``route``::

    Pyramid.add_route('route name', '/my/path')

.. note::

    The function ``add_route`` is just a wrapper of `add_route
    <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
    config.html#pyramid.config.Configurator.add_route>`_

    The args already filled by the wraper are:

    * name: is the **route name**
    * pattern: is the path

.. warning::

    It 's important to use the add_route of Pyramid, because
    when the view are add in configuration, this view check is the
    **route name** exist in the routes.

Pyramid controller which depend of the installation of the bloks
----------------------------------------------------------------

Theses controllers must be `declared in the bloks
<http://doc.anyblok.org/HOWTO_CREATE_APP.html#create-bloks>`_

The declaration of theses controllers is as the declaration of `AnyBlok Model
<http://doc.anyblok.org/HOWTO_CREATE_APP.html#create-models>`_

They are three controllers which can be declared in the bloks:

* PyramidHTTP
* PyramidJsonRPC
* PyramidXmlRPC

The controller can be inherited by ``Mixin``

* PyramidMixin

The controller inherit also ``Core`` and have some feature as:

* Cache
* Properties

HTTP controller
~~~~~~~~~~~~~~~

Get the ``Type`` of controller::

    from anyblok import Declarations
    PyramidHTTP = Declarations.PyramidHTTP
    register = Declarations.register

Declare a ``view``::

    @register(PyramidHTTP)
    class MyController:

        @PyramidHTTP.view()
        def myview(request):
            # route name == myview
            ...

        @PyramidHTTP.view('myroute')
        def myotherview(request):
            # route name == myroute
            ...

.. note::

    The decorator ``view`` is just a wrapper of `add_view
    <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
    config.html#pyramid.config.Configurator.add_view>`_

    the args already filled by the wraper are:

    * view: is the decorated function
    * name: the default value is the name of the method or the first args

Declare a ``route``::

    PyramidHTTP.add_route('route name', '/my/path')

.. note::

    The function ``add_route`` is just a wrapper of `add_route
    <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
    config.html#pyramid.config.Configurator.add_route>`_

    The args already filled by the wraper are:

    * name: is the **route name**
    * pattern: is the path

.. warning::

    It 's important to use the add_route of PyramidHTTP, because
    when the view are add in configuration, this view check is the
    **route name** exist in the routes.


JSON-RPC controller
~~~~~~~~~~~~~~~~~~~

Get the ``Type`` of controller::

    from anyblok import Declarations
    PyramidJsonRPC = Declarations.PyramidJsonRPC
    register = Declarations.register

Declare a ``rpc method``::

    @register(PyramidJsonRPC)
    class MyController:

        @PyramidJsonRPC.rpc_method()
        def mymethod(request):
            # method name == mymethod
            ...

        @PyramidJsonRPC.rpc_method('myroute')
        def myothermethod(request):
            # method name == myroute
            ...

.. note::

    The decorator ``rpc_method`` is just a wrapper of `add_jsonrpc_method
    <http://docs.pylonsproject.org/projects/pyramid-rpc/en/latest/
    jsonrpc.html#pyramid_rpc.jsonrpc.add_jsonrpc_method>`_

    the args already filled by the wraper are:

    * view: is the decorated method
    * endpoint: the default value is the name of the method or the first
        args

Declare a ``route``::

    PyramidJsonRPC.add_route(PyramidJsonRPC.MyController, '/my/path')

.. note::

    The function ``add_route`` is just a wrapper of `add_jsonrpc_endpoint
    <http://docs.pylonsproject.org/projects/pyramid-rpc/en/latest/
    jsonrpc.html#pyramid_rpc.jsonrpc.add_jsonrpc_endpoint>`_

    The args already filled by the wraper are:

    * name: is the **route name**
    * pattern: is the path

.. warning::

    It 's important to use the add_route of PyramidJsonRPC, because
    when the view are add in configuration, this view check is the
    **rpc method** exist in the routes.

XML-RPC controller
~~~~~~~~~~~~~~~~~~

Get the ``Type`` of controller::

    from anyblok import Declarations
    PyramidXmlRPC = Declarations.PyramidXmlRPC
    register = Declarations.register

Declare a ``rpc method``::

    @register(PyramidXmlRPC)
    class MyController:

        @PyramidXmlRPC.rpc_method()
        def mymethod(request):
            # method name == mymethod
            ...

        @PyramidXmlRPC.rpc_method('myroute')
        def myothermethod(request):
            # method name == myroute
            ...

.. note::

    The decorator ``rpc_method`` is just a wrapper of `add_xmlrpc_method
    <http://docs.pylonsproject.org/projects/pyramid-rpc/en/latest/
    xmlrpc.html#pyramid_rpc.xmlrpc.add_xmlrpc_method>`_

    the args already filled by the wraper are:

    * view: is the decorated method
    * endpoint: the default value is the name of the method or the first
        args

Declare a ``route``::

    PyramidXmlRPC.add_route(PyramidXmlRPC.MyController, '/my/path')

.. note::

    The function ``add_route`` is just a wrapper of `add_xmlrpc_endpoint
    <http://docs.pylonsproject.org/projects/pyramid-rpc/en/latest/
    xmlrpc.html#pyramid_rpc.xmlrpc.add_xmlrpc_endpoint>`_

    The args already filled by the wraper are:

    * name: is the **route name**
    * pattern: is the path

.. warning::

    It 's important to use the add_route of PyramidXmlRPC, because
    when the view are add in configuration, this view check is the
    **rpc method** exist in the routes.

Pyramid ``Mixin``
~~~~~~~~~~~~~~~~~

Mixin is used to define behaviours on the controllers.


Declare a ``Mixin``::

    from anyblok import Declarations
    register = Declarations.register
    PyramidMixin = Declarations.PyramidMixin


    @register(PyramidMixin)
    class MyMixin:
        ...

Inherit a ``Mixin`` by a controller::

    @register(PyramidHTTP)
    class MyController(PyramidMixin.MyMixin):
        ...

Inherit a ``Mixin`` by another ``Mixin``::

    @register(PyramidMixin)
    class MyAnotherMixin(PyramidMixin.MyMixin):
        ...


Inheritance
~~~~~~~~~~~

The conbroller can inherit ``PyramidMixin`` and also Controller of the same
``Type``::

    @register(PyramidHTTP)
    class MyController(PyramidHTTP.OtherController):
        ...

Pyramid ``Core``
~~~~~~~~~~~~~~~~

The ``Core`` used by the controller are:

* ControllerBase: For all the controller
* ControllerHTTP
* ControllerRPC
* ControllerJsonRPC
* ControllerXmlRPC

Overload a ``Core``::

    @register(Core)
    class ControllerBase:
        ...

Cache
~~~~~

Add a cache on a controller is as `cache on a model
<http://doc.anyblok.org/MEMENTO.html#cache>`_.

Declare a cache on a controller::

    @register(PyramidHTTP):
    class MyController:

        @classmethod_method()
        def mycachedmethod(cls):
            ...

Declare a cache on a ``Mixin``::

    @registry(PyramidMixin)
    class MyMixin:

        @classmethod_method()
        def mycachedmethod(cls):
            ...

    @register(PyramidHTTP):
    class MyController(PyramidMixin.MyMixin):
        ...

Declare a cache on a ``Core``::

    @registry(Core)
    class PyramidBase:

        @classmethod_method()
        def mycachedmethod(cls):
            ...

    @register(PyramidHTTP):
    class MyController:
        ...

.. warning::

    The instance of controller are not the same for each call. Then use
    ``Declarations.cache`` to cache in only one request else use
    ``Declarations.classmethod_cache`` to cache a method for all the request

Properties
~~~~~~~~~~

the decorator ``*Controller*.check_properties`` allow to define an property
to check before the ``view`` or ``rpc_method`` be called.

This property check if the *user* is authentificated::

    @register(PyramidHTTP)
    class MyController:

        def check_property_myproperty(self, value):
            """If the value property is not good the this method must raise"""

        @check_properties(myproperty=OneValue)
        @PyramidHTTP.view()
        def myview(self):
            ...

You can add your property but the property must be associated at a check
method on the controller. This method can be in a ``Mixin`` or in a ``Core``.
This method can be overload.
