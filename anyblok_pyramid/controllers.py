from anyblok import Declarations
from anyblok.common import TypeList, apply_cache
from anyblok.registry import RegistryManager
from pyramid_rpc.mapper import MapplyViewMapper
from anyblok.mixin import MixinType


def mapply(self, ob, positional, keyword):
    return ob(*positional, **keyword)

MapplyViewMapper.mapply = mapply


RegistryManager.declare_core('PyramidBaseRPC')
RegistryManager.declare_core('PyramidBaseJsonRPC')
RegistryManager.declare_core('PyramidBaseXmlRPC')


@Declarations.register(Declarations.Exception)
class PyramidException(Exception):
    """ Exception for web type """


@Declarations.add_declaration_type(isAnEntry=True)
class PyramidMixin(MixinType):
    pass


# Not depend of the registry
@Declarations.add_declaration_type()
class Pyramid:

    routes = []
    views = []

    @classmethod
    def register(cls, parent, name, cls_, **kwargs):
        raise Declarations.Exception.PyramidException(
            'Register declaration of one Pyramid type is forbidden')

    @classmethod
    def unregister(cls, child, cls_):
        raise Declarations.Exception.PyramidException(
            'Unregister declaration of one Pyramid type is forbidden')

    @classmethod
    def add_route(cls, path, endpoint):
        key = (endpoint, path)
        if key not in cls.routes:
            cls.routes.append(key)

    @classmethod
    def add_view(cls, endpoint, **kwargs):
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


class PyramidRPC:

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

        if _registryname not in cls.methods:
            cls.methods[_registryname] = {}

        rpc_methods = RegistryManager.get_entry_properties_in_register(
            cls.__name__, _registryname).get('rpc_methods', {})

        for attr in dir(cls_):
            if hasattr(getattr(cls_, attr), 'rpc_method'):
                rpc_method = getattr(cls_, attr).rpc_method
                method = rpc_method['method']
                if method not in cls.methods[_registryname]:
                    cls.methods[_registryname][method] = {}

                cls.methods[_registryname][method].update(rpc_method)

                if method not in rpc_methods:
                    rpc_methods[method] = {}

                rpc_methods[method].update(rpc_method)

        kwargs.update({
            '__registry_name__': _registryname,
            'rpc_methods': rpc_methods,
        })

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
    def hook_insert_in_bases(cls, registry, bases):
        pass

    @classmethod
    def rpc_method(cls, **kwargs):
        def wraper(function):
            kwargs['function'] = function.__name__
            if 'method'not in kwargs:
                kwargs['method'] = function.__name__

            function.rpc_method = kwargs
            return function

        return wraper

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
            bases.extend(registry.loaded_cores['PyramidBaseRPC'])
            bases.append(registry.registry_base)
            base = type(namespace, tuple(bases), properties)
            registry.loaded_controllers[namespace] = base
            bases = [base]

        return bases

    @classmethod
    def assemble_callback(cls, registry):
        if not hasattr(registry, 'loaded_controllers'):
            registry.loaded_controllers = {}

        for namespace in registry.loaded_registries[cls.__name__ + '_names']:
            cls.load_namespace(registry, namespace)

    @classmethod
    def add_route(cls, path, registryname):
        key = (registryname.__registry_name__, path)
        if key not in cls.routes:
            cls.routes.append(key)


@Declarations.add_declaration_type(isAnEntry=True,
                                   assemble='assemble_callback')
class PyramidJsonRPC(PyramidRPC):
    """
    """

    methods = {}
    routes = []

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        bases.extend(registry.loaded_cores['PyramidBaseJsonRPC'])


@Declarations.add_declaration_type(isAnEntry=True,
                                   assemble='assemble_callback')
class PyramidXmlRPC(PyramidRPC):
    """
    """

    methods = {}
    routes = []

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        bases.extend(registry.loaded_cores['PyramidBaseXmlRPC'])


class Handler:
    def __init__(self, namespace, method, function):
        self.namespace = namespace
        self.method = method
        self.function = function

    def wrap_view(self, request, *args, **kwargs):
        registry = RegistryManager.get(request.session['database'])
        return getattr(registry.loaded_controllers[self.namespace](),
                       self.function)(*args, **kwargs)


def pyramid_config(config):
    for route in Pyramid.routes:
        config.add_route(*route)

    for function, properties in Pyramid.views:
        config.add_view(function, **properties)


def _pyramid_rpc_config(cls, add_endpoint, add_method):
    for route in cls.routes:
        add_endpoint(*route)

    endpoints = [x[0] for x in cls.routes]
    for namespace in cls.methods:
        if namespace not in endpoints:
            raise PyramidException(
                "One or more %s controller has been declared but no route have"
                " declared" % namespace)
        for method in cls.methods[namespace]:
            rpc_method = cls.methods[namespace][method]
            function = rpc_method.pop('function')
            add_method(Handler(namespace, method, function).wrap_view,
                       route_name=namespace,
                       **rpc_method)


def pyramid_jsonrpc_config(config):
    _pyramid_rpc_config(
        PyramidJsonRPC, config.add_jsonrpc_endpoint, config.add_jsonrpc_method)


def pyramid_xmlrpc_config(config):
    _pyramid_rpc_config(
        PyramidXmlRPC, config.add_xmlrpc_endpoint, config.add_xmlrpc_method)
