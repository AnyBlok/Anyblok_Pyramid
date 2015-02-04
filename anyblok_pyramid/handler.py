from anyblok import Declarations
from anyblok.registry import RegistryManager


class Handler:

    def init_controller(self, request):
        registry = RegistryManager.get(request.session['database'])
        if self.namespace not in registry.loaded_controllers:
            raise Declarations.Exception.HandlerException(
                "Unknow controller %r" % self.namespace)

        self.controller = registry.loaded_controllers[self.namespace](
            request)

    def call_controller(self, *args, **kwargs):
        return getattr(self.controller, self.function)(*args, **kwargs)


class HandlerHTTP(Handler):

    def __init__(self, namespace, view):
        self.namespace = namespace
        self.view = view

    def wrap_view(self, request):
        self.init_controller(request)

        args = []
        kwargs = {}
        if request.method in ('POST', 'PUT', 'DELETE'):
            kwargs.update(dict(request.params))
        else:
            args.extend(list(request.params))

        self.function = self.controller.get_function_from_view(self.view)
        self.controller.check_function(self.function)
        return self.call_controller(*args, **kwargs)


class HandlerRPC(Handler):

    def __init__(self, namespace, method):
        self.namespace = namespace
        self.method = method

    def wrap_view(self, request, *args, **kwargs):
        self.init_controller(request)
        self.function = self.controller.get_function_from_method(self.method)
        self.controller.check_function(self.function)
        return self.call_controller(*args, **kwargs)
