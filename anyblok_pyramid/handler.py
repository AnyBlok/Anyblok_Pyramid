from anyblok.registry import RegistryManager


class Handler:

    def __init__(self, namespace, function):
        self.namespace = namespace
        self.function = function

    def call_controller(self, request, *args, **kwargs):
        registry = RegistryManager.get(request.session['database'])
        return getattr(registry.loaded_controllers[self.namespace](),
                       self.function)(*args, **kwargs)


class HandlerHTTP(Handler):

    def wrap_view(self, request, *args, **kwargs):
        return self.call_controller(request, *args, **kwargs)


class HandlerRPC(Handler):
    def __init__(self, namespace, method, function):
        super(HandlerRPC, self).__init__(namespace, function)
        self.method = method

    def wrap_view(self, request, *args, **kwargs):
        return self.call_controller(request, *args, **kwargs)
