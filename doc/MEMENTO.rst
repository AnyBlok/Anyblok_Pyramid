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

WorkingSet
----------

Anyblok / Pyramid add two function to use callback:

* `set_callable`: save a callback, the name of the callable is the name of the callback
* `get_callable`: return a callback in function of this name

for exemple, see the callable `get_registry`::

    registry = get_callable('get_registry')(request)

Authentication and authorization
--------------------------------

Authentication can be add directly in configuration with includeme.

Links to the official documentation :

* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/design.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authorization.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authentication.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/quick_tutorial/authorization.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/quick_tutorial/authentication.html

Link to an official tutorial
If you want to replace default pyramid component by your own:

* http://docs.pylonsproject.org/projects/pyramid//en/latest/narr/security.html#creating-your-own-authentication-policy
* http://docs.pylonsproject.org/projects/pyramid//en/latest/narr/security.html#creating-your-own-authorization-policy

Add a root factory::

    class RootFactory(object):

        def __init__(self, request):
            self.request = request

        __acl__ = [
            (Allow, Everyone, 'all'),
        ]

Add the authentication callback::

    def group_finder(email, request):
        return ("all",)

Add the includeme callable::

    def pyramid_security_config(config):
        # Authentication policy
        secret = Configuration.get("authn_key", "secret")
        authn_policy = AuthTktAuthenticationPolicy(secret=secret,
                                                   callback=group_finder)
        config.set_authentication_policy(authn_policy)
        # Authorization policy
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
        # Root factory: only added if set in config file (no default one)
        config.set_root_factory(RootFactory)

Add the includeme in the entry point::

        setup(
            ...,
            entry_points={
                'anyblok_pyramid.includeme': [
                    'pyramid_security_config=path:pyramid_security_config',
                    ...
                ],
            },
            ...,
        )

.. note::

    You can get the session, with the callback get_registry::

        from anyblok_pyramid import get_callable
        # only if get_registry is implemented for you use case
        registry = get_callable('get_registry')(request)

.. note::

    You can merge the authorization of Pyramid and the authorization of AnyBlok

JSON adapter
------------

In the case where you need to return json value you can format the data with:

* Define an adapter for the python ``type``::

    def datetime_adapter(obj, request):
        return obj.isoformat()

* Add the adapter at the pyramid configuration::

    def declare_json_data_adapter(config):
        from pyramid.renderers import JSON
        json_renderer = JSON()
        json_renderer.add_adapter(datetime, datetime_adapter)
        config.add_renderer('json', json_renderer)

* Add the includeme::

    setup(
        ...,
        entry_points={
            'anyblok_pyramid.includeme': [
                'json_adapter=path:declare_json_data_adapter',
                ...
            ],
        },
        ...,
    )
