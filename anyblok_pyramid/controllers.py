# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.common import TypeList, apply_cache
from anyblok.registry import RegistryManager
from pyramid_rpc.mapper import MapplyViewMapper
from anyblok.mixin import MixinType


# Monkey patch the method which check the good args and kwargs of the callback
# method of pyramid_rpc because the Handler have not the good parameter
# and can not have the good parameters for eache declarated view
def mapply(self, ob, positional, keyword):
    return ob(*positional, **keyword)

MapplyViewMapper.mapply = mapply


# Declara new Core only for Pyramid Types
RegistryManager.declare_core('PyramidBase')
RegistryManager.declare_core('PyramidBaseHTTP')
RegistryManager.declare_core('PyramidBaseRPC')
RegistryManager.declare_core('PyramidBaseJsonRPC')
RegistryManager.declare_core('PyramidBaseXmlRPC')


@Declarations.register(Declarations.Exception)
class PyramidException(Exception):
    """ Exception for web type """


@Declarations.add_declaration_type(isAnEntry=True)
class PyramidMixin(MixinType):
    """ The PyramidMixin class are used to define a behaviours on models:

    * Add new mixin class::

        @Declarations.register(Declarations.PyramidMixin)
        class MyMixinclass:
            pass

    * Remove a mixin class::

        Declarations.unregister(Declarations.PyramidMixin.MyMixinclass,
                                MyMixinclass)
    """


# Not depend of the registry
@Declarations.add_declaration_type()
class Pyramid:
    """ The Pyramid controller is a simple wrapper of the Pyramid controller

    Pyramid can scan easily the ``view`` declarations to add them in the
    configuration. But the ``route`` have to add directlly in the
    configuration. This controller do all of them. The ``route`` and ``view``
    are saved in the controller and the controller add them in the
    configuration at the start of the wsgi server

    .. warning::

        This case is only use by the script ``anyblok_wsgi``, if you use an
        another script, you must include the includem ``pyramid_config``
        or use the function ``make_config`` to get all the configuration

    This ``Type`` is not an entry, no class are assembled in the registry.
    You must not add any class of this ``Type``, the methods ``register`` and
    ``unregister`` raise an exception.

    Add a view::

        from anyblok import Declarations


        @Declarations.Pyramid.add_view('route name')
        def myview(request):
            ...

    .. note::

        The decorator ``add_view`` is just a wrapper of `add_view
        <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
        config.html#pyramid.config.Configurator.add_view>`_

        the args already filled by the wraper are:

        * view: is the decorated function
        * name: is the **route name**

    Add a route::

        from anyblok import Declarations


        Declarations.Pyramid.add_route('route name', '/my/path')

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

    """

    routes = []
    """Route properties to add in pyramid configuration"""
    views = []
    """View properties to add in pyramid configuration"""

    @classmethod
    def register(cls, parent, name, cls_):
        """ **Forbidden method**, this method always raise when calls

        :param parent: Existing global registry
        :param name: Name of the new registry to add it
        :param cls_: Class Interface to add in registry
        :exception: PyramidException
        """
        raise Declarations.Exception.PyramidException(
            'Register declaration of one Pyramid type is forbidden')

    @classmethod
    def unregister(cls, child, cls_):
        """ **Forbidden method**, this method always raise when calls

        :param entry: entry declaration of the model where the ``cls_``
            must be removed
        :param cls_: Class Interface to remove in registry
        :exception: PyramidException
        """
        raise Declarations.Exception.PyramidException(
            'Unregister declaration of one Pyramid type is forbidden')

    @classmethod
    def add_route(cls, *args, **kwargs):
        """ Declare a route to add it in the configuration of ``Pyramid``::

            from anyblok import Declarations


            Declarations.Pyramid.add_route('route name', '/my/path')

        .. note::

            The function ``add_route`` is just a wrapper of `add_route
            <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
            config.html#pyramid.config.Configurator.add_route>`_

            The args already filled by the wraper are:

            * name: is the **route name**
            * pattern: is the path

        """
        key = (args, kwargs)
        cls.routes.append(key)

    @classmethod
    def add_view(cls, endpoint, **kwargs):
        """ Declare a view to add it in the configuration of ``Pyramid``::

            from anyblok import Declarations


            @Declarations.Pyramid.add_view('route name')
            def myview(request):
                ...

        .. note::

            The decorator ``add_view`` is just a wrapper of `add_view
            <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
            config.html#pyramid.config.Configurator.add_view>`_

            the args already filled by the wraper are:

            * view: is the decorated function
            * name: is the **route name**

        """
        def wraper(function):
            def wraper_function(request):
                request_kwargs = request.matchdict
                request_kwargs.update(dict(request.params))
                return function(request, **request_kwargs)

            properties = {'route_name': endpoint}
            properties.update(kwargs)
            cls.views.append((wraper_function, properties))
            return function

        return wraper


class PyramidBase:
    """
    .. warning::

        This class is not a controller, but base of HTTP and RPC controller

    .. warning::

        This class is not the ``Core.PyramidBase``.

    The declarations of HTTP and RPC controller is not the same, but they are
    few difference.
    """

    @classmethod
    def register(cls, parent, name, cls_, **kwargs):
        """ add new sub registry in the registry

        :param parent: Existing global registry
        :param name: Name of the new registry to add it
        :param cls_: Class Interface to add in registry
        """
        _registryname = parent.__registry_name__ + '.' + name
        if not hasattr(parent, name):

            p = {
                '__registry_name__': _registryname,
            }
            ns = type(name, tuple(), p)
            setattr(parent, name, ns)

        if parent is Declarations:
            return

        kwargs.update({'__registry_name__': _registryname})
        kwargs.update(cls.hook_view_from_decorators(_registryname, cls_))
        kwargs.update(cls.properties_from_decorators(_registryname, cls_))

        RegistryManager.add_entry_in_register(
            cls.__name__, _registryname, cls_, **kwargs)

    @classmethod
    def unregister(cls, entry, cls_):
        """ Remove the Interface from the registry

        :param entry: entry declaration of the model where the ``cls_``
            must be removed
        :param cls_: Class Interface to remove in registry
        """
        RegistryManager.remove_in_register(cls_)

    @classmethod
    def properties_from_decorators(cls, registryname, cls_):
        """ Properties is  used to make some check before  call the
        view. This method get the view which are need this verification

        :param registryname: the registry name
        :param cls_: a class of the registry name to take the properties
        :rtype: dict to save in the registry
        """
        properties = RegistryManager.get_entry_properties_in_register(
            cls.__name__, registryname).get('properties', {})

        for attr in dir(cls_):
            if hasattr(getattr(cls_, attr), 'properties'):
                if attr not in properties:
                    properties[attr] = {}

                properties[attr].update(getattr(cls_, attr).properties)

        return {'properties': properties}

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        """ The difference between HTTP and RPC controller are the Core used
        by them. all of them must inherit of:

        * Core.PyramidBase
        * registry_base

        :param registry: the current registry for the controller
        :param bases: bases list which define the controller
        """
        bases.extend(registry.loaded_cores['PyramidBase'])
        bases.append(registry.registry_base)

    @classmethod
    def transform_base(cls, registry, namespace, base, properties):
        """ Detect specific declaration which must define by registry

        :param registry: the current registry
        :param namespace: the namespace of the controller
        :param base: One of the base of the controller
        :param properties: the properties of the controller
        :rtype: new base
        """
        new_base = apply_cache(registry, namespace, base, properties)
        return new_base

    @classmethod
    def load_namespace(cls, registry, namespace, realregistryname=None):
        """ Return the bases and the properties of the namespace

        :param registry: the current registry
        :param namespace: the namespace of the model
        :param realregistryname: the name of the model if the namespace is a
            mixin
        :rtype: the list od the bases and the properties
        :exception: PyramidException
        """
        if namespace in registry.loaded_namespaces:
            return [registry.loaded_controllers[namespace]]

        bases = TypeList(cls, registry, namespace)
        ns = registry.loaded_registries[namespace]
        properties = ns['properties'].copy()

        for b in ns['bases']:
            if b in bases:
                continue

            if realregistryname:
                bases.append(b, namespace=realregistryname)
            else:
                bases.append(b)

            for b_ns in b.__anyblok_bases__:
                brn = b_ns.__registry_name__
                if brn in registry.loaded_registries['PyramidMixin_names']:
                    if realregistryname:
                        bases.extend(cls.load_namespace(
                            registry, brn, realregistryname=realregistryname))
                    else:
                        bases.extend(cls.load_namespace(
                            registry, brn, realregistryname=namespace))
                elif brn in registry.loaded_registries[cls.__name__ + '_names']:
                    bases.extend(cls.load_namespace(registry, brn))
                else:
                    raise PyramidException(
                        "You have not to inherit the %r "
                        "Only the 'PyramidMixin' and %r are allowed" % (
                            brn, cls.__name__))

        if namespace in registry.loaded_registries[cls.__name__ + '_names']:
            cls.hook_insert_in_bases(registry, bases)
            base = type(namespace, tuple(bases), properties)
            registry.loaded_controllers[namespace] = base
            bases = [base]

        return bases

    @classmethod
    def assemble_callback(cls, registry):
        """ Assemble callback is called to assemble all the controllers
        from the installed bloks

        :param registry: registry to update
        """
        if not hasattr(registry, 'loaded_controllers'):
            registry.loaded_controllers = {}

        for namespace in registry.loaded_registries[cls.__name__ + '_names']:
            cls.load_namespace(registry, namespace)

    @classmethod
    def check_properties(cls, **kwargs):
        """ decorator which add the properties to check

        :param \*\*kwargs: dict property: value to check
        """
        def wraper(function):
            function.properties = kwargs
            return function

        return wraper

    @classmethod
    def authentificated(cls):
        """ Decorator which add the property ``authentificated`` with the value
        ``True``
        """
        def wraper(function):
            function.properties = {'authentificated': True}
            return function

        return wraper


@Declarations.add_declaration_type(isAnEntry=True,
                                   assemble='assemble_callback')
class PyramidHTTP(PyramidBase):
    """ The PyramidHTTP controller is a simple wrapper of the Pyramid
    controller

    At the start of the pyramid server, all routes and all the views must be
    known. But the routes and views are declared on the bloks. Then the
    declaration of the routes and the views must be done also if the bloks
    are not installed. When the controller is called then the view must be
    validated by the controller to be called

    .. warning::

        This case is only use by the script ``anyblok_wsgi``, if you use an
        another script, you must include the includem ``pyramid_http_config``
        or use the function ``make_config`` to get all the configuration

    Add a view::

        from anyblok import Declarations


        @Declarations.register(Declaration.PyramidHTTP)
        class MyController:

            @Declaration.PyramidHTTP.view()
            def myview(request):
                # route name == myview
                ...

            @Declaration.PyramidHTTP.view('myroute')
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

    Add a route::

        from anyblok import Declarations


        Declarations.PyramidHTTP.add_route('route name', '/my/path')

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

    """

    routes = []
    """Route properties to add in pyramid configuration"""
    views = {}
    """View properties to add in pyramid configuration"""

    @classmethod
    def hook_view_from_decorators(cls, registryname, cls_):
        """ Save the decorated method by view

        :param registryname: registry name of the controller
        :param cls\_: the cls of the registry name
        :rtype: dict {'views': {route name: function} }
        """
        views = RegistryManager.get_entry_properties_in_register(
            cls.__name__, registryname).get('views', {})

        for attr in dir(cls_):
            if hasattr(getattr(cls_, attr), 'view'):
                view = getattr(cls_, attr).view
                rn = view['route_name']
                key = (registryname, rn)
                if key not in cls.views:
                    cls.views[key] = {}

                cls.views[key].update(view)
                views[rn] = attr

        return {'views': views}

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        """ Define the Core class inherited by PyramidHTTP controllers

        * Core.PyramidBaseHTTP
        * super()

        :param registry: the current registry for the controller
        :param bases: bases list which define the controller
        """
        bases.extend(registry.loaded_cores['PyramidBaseHTTP'])
        super(PyramidHTTP, cls).hook_insert_in_bases(registry, bases)

    @classmethod
    def view(cls, **kwargs):
        """ Declare a view to add it in the configuration of ``Pyramid``::

            from anyblok import Declarations


            @Declarations.register(Declaration.PyramidHTTP)
            class My controller:

                @Declaration.PyramidHTTP.view()
                def myview(request):
                    # route name == myview
                    ...

                @Declaration.PyramidHTTP.view('myroute')
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

        """
        def wraper(function):
            if 'route_name' not in kwargs:
                kwargs['route_name'] = function.__name__

            function.view = kwargs
            return function

        return wraper

    @classmethod
    def add_route(cls, *args, **kwargs):
        """ Declare a route to add it in the configuration of ``Pyramid``::

            from anyblok import Declarations


            Declarations.PyramidHTTP.add_route('route name', '/my/path')

        .. note::

            The function ``add_route`` is just a wrapper of `add_route
            <http://docs.pylonsproject.org/docs/pyramid/en/latest/api/
            config.html#pyramid.config.Configurator.add_route>`_

            The args already filled by the wraper are:

            * name: is the **route name**
            * pattern: is the path

        """
        cls.routes.append((args, kwargs))


class PyramidRPC(PyramidBase):

    @classmethod
    def hook_view_from_decorators(cls, registryname, cls_):
        """ Save the decorated method by rpc method

        :param registryname: registry name of the controller
        :param cls\_: the cls of the registry name
        :rtype: dict {'views': {route name: function} }
        """
        if registryname not in cls.methods:
            cls.methods[registryname] = {}

        rpc_methods = RegistryManager.get_entry_properties_in_register(
            cls.__name__, registryname).get('rpc_methods', {})

        for attr in dir(cls_):
            if hasattr(getattr(cls_, attr), 'rpc_method'):
                rpc_method = getattr(cls_, attr).rpc_method
                method = rpc_method['method']
                if method not in cls.methods[registryname]:
                    cls.methods[registryname][method] = {}

                cls.methods[registryname][method].update(rpc_method)
                rpc_methods[method] = attr

        return {'rpc_methods': rpc_methods}

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        """ Define the Core class inherited by Pyramid RPC controllers

        * Core.PyramidBaseRPC
        * super()

        :param registry: the current registry for the controller
        :param bases: bases list which define the controller
        """
        bases.extend(registry.loaded_cores['PyramidBaseRPC'])
        super(PyramidRPC, cls).hook_insert_in_bases(registry, bases)

    @classmethod
    def rpc_method(cls, **kwargs):
        """ Declare a rpc method to add it in the configuration of
        ``Pyramid RPC``"""
        def wraper(function):
            if 'method'not in kwargs:
                kwargs['method'] = function.__name__

            function.rpc_method = kwargs
            return function

        return wraper

    @classmethod
    def add_route(cls, *args, **kwargs):
        """ Declare a route to add it in the configuration of ``Pyramid``"""
        if len(args) == 1:
            args = (args[0].__registry_name__,)
        elif args:
            args = list(args)
            args = tuple([args[0].__registry_name__] + args[1:])
        elif 'endpoint' in kwargs:
            kwargs['endpoint'] = kwargs['endpoint'].__registry_name__
        elif 'route_name' in kwargs:
            kwargs['route_name'] = kwargs['route_name'].__registry_name__
        cls.routes.append((args, kwargs))


@Declarations.add_declaration_type(isAnEntry=True,
                                   assemble='assemble_callback')
class PyramidJsonRPC(PyramidRPC):
    """ The PyramidJsonRPC controller is a simple wrapper of the Pyramid
    JSON-RPC controller

    At the start of the pyramid server, all routes and all the rpc methods
    must be known. But the routes and rpc methods are declared on the bloks.
    Then  the declaration of the routes and the rpc methods must be done also
    if the bloks are not installed. When the controller is called then the rpc
    method must be validated by the controller to be called

    .. warning::

        This case is only use by the script ``anyblok_wsgi``, if you use an
        another script, you must include the includem
        ``pyramid_jsonrpc_config`` or use the function ``make_config``
        to get all the configuration

    Add a rpc method::

        from anyblok import Declarations


        @Declarations.register(Declaration.PyramidJsonRPC)
        class MyController:

            @Declaration.PyramidJsonRPC.rpc_method()
            def mymethod(request):
                # method name == mymethod
                ...

            @Declaration.PyramidJsonRPC.rpc_method('myroute')
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

    Add a route::

        from anyblok import Declarations


        Declarations.PyramidJsonRPC.add_route(
            Declarations.PyramidJsonRPC.MyController, '/my/path')

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

    """

    routes = []
    """Route properties to add in pyramid configuration"""
    methods = {}
    """RPC method properties to add in pyramid configuration"""

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        """ Define the Core class inherited by PyramidJsonRPC controllers

        * Core.PyramidBaseJsonRPC
        * super()

        :param registry: the current registry for the controller
        :param bases: bases list which define the controller
        """
        bases.extend(registry.loaded_cores['PyramidBaseJsonRPC'])
        super(PyramidJsonRPC, cls).hook_insert_in_bases(registry, bases)


@Declarations.add_declaration_type(isAnEntry=True,
                                   assemble='assemble_callback')
class PyramidXmlRPC(PyramidRPC):
    """ The PyramidXmlRPC controller is a simple wrapper of the Pyramid
    XML-RPC controller

    At the start of the pyramid server, all routes and all the rpc methods
    must be known. But the routes and rpc methods are declared on the bloks.
    Then  the declaration of the routes and the rpc methods must be done also
    if the bloks are not installed. When the controller is called then the rpc
    method must be validated by the controller to be called

    .. warning::

        This case is only use by the script ``anyblok_wsgi``, if you use an
        another script, you must include the includem
        ``pyramid_xmlrpc_config`` or use the function ``make_config``
        to get all the configuration

    Add a rpc method::

        from anyblok import Declarations


        @Declarations.register(Declaration.PyramidXmlRPC)
        class MyController:

            @Declaration.PyramidXmlRPC.rpc_method()
            def mymethod(request):
                # method name == mymethod
                ...

            @Declaration.PyramidXmlRPC.rpc_method('myroute')
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

    Add a route::

        from anyblok import Declarations


        Declarations.PyramidXmlRPC.add_route(
            Declarations.PyramidXmlRPC.MyController, '/my/path')

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

    """

    routes = []
    """Route properties to add in pyramid configuration"""
    methods = {}
    """RPC method properties to add in pyramid configuration"""

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        """ Define the Core class inherited by PyramidXmlRPC controllers

        * Core.PyramidBaseXmlRPC
        * super()

        :param registry: the current registry for the controller
        :param bases: bases list which define the controller
        """
        bases.extend(registry.loaded_cores['PyramidBaseXmlRPC'])
        super(PyramidXmlRPC, cls).hook_insert_in_bases(registry, bases)
