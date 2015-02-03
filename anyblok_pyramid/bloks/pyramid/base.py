from anyblok import Declarations


@Declarations.register(Declarations.Core)
class PyramidBase:

    def __init__(self, request):
        self.request = request
        self.session = request.session


@Declarations.register(Declarations.Core)
class PyramidBaseHTTP:

    def check_function(self, function):
        if not hasattr(self, function):
            raise Declarations.Exception.PyramidException(
                "%s has not %s function" % (self.__registry_name__, function))


@Declarations.register(Declarations.Core)
class PyramidBaseRPC:

    def check_method(self, function):
        pass
