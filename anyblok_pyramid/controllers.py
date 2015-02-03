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


class PyramidBase:

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


class PyramidHTTP(PyramidBase):

    routes = []
    views = {}

    @classmethod
    def hook_view_from_decorators(cls, registryname, cls_):
        views = RegistryManager.get_entry_properties_in_register(
            cls.__name__, registryname).get('views', [])

        for attr in dir(cls_):
            if hasattr(getattr(cls_, attr), 'view'):
                view = getattr(cls_, attr).view
                key = (registryname, view['function'])
                if key not in cls.views:
                    cls.views[key] = {}

                cls.views[key].update(view)

                if key not in views:
                    views.append(key)

        return {'views': view}

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        bases.extend(registry.loaded_cores['PyramidBaseHTTP'])
        super(PyramidRPC, cls).hook_insert_in_bases(registry, bases)

    @classmethod
    def view(cls, **kwargs):
        def wraper(function):
            kwargs['function'] = function.__name__
            function.view = kwargs
            return function

        return wraper


class PyramidRPC(PyramidBase):

    @classmethod
    def hook_view_from_decorators(cls, registryname, cls_):
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

                if method not in rpc_methods:
                    rpc_methods[method] = {}

                rpc_methods[method].update(rpc_method)

        return {'rpc_methods': rpc_methods}

    @classmethod
    def hook_insert_in_bases(cls, registry, bases):
        bases.extend(registry.loaded_cores['PyramidBaseRPC'])
        super(PyramidRPC, cls).hook_insert_in_bases(registry, bases)

    @classmethod
    def rpc_method(cls, **kwargs):
        def wraper(function):
            kwargs['function'] = function.__name__
            if 'method'not in kwargs:
                kwargs['method'] = function.__name__

            function.rpc_method = kwargs
            return function

        return wraper


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
        super(PyramidJsonRPC, cls).hook_insert_in_bases(registry, bases)


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
        super(PyramidXmlRPC, cls).hook_insert_in_bases(registry, bases)
