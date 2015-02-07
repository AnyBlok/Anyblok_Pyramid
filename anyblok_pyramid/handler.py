# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.registry import RegistryManager


@Declarations.register(Declarations.Exception.PyramidException)
class HandlerException(Declarations.Exception.PyramidException):
    """ Simple exception for handler """


class Handler:
    """ Base class for all the pyramid handler. """

    def init_controller(self, request):
        """ Get an instance of the controller

        :param request: http request get from pyramid
        :rtype: instance of Pyramid controller
        :exception: HandlerException
        """
        registry = RegistryManager.get(request.session['database'])
        registry.System.Cache.clear_invalidate_cache()
        if self.namespace not in registry.loaded_controllers:
            raise Declarations.Exception.HandlerException(
                "Unknow controller %r" % self.namespace)

        self.controller = registry.loaded_controllers[self.namespace](
            request)

    def call_controller(self, *args, **kwargs):
        """ call the controller function and return the result """
        return getattr(self.controller, self.function)(*args, **kwargs)


class HandlerHTTP(Handler):
    """ Handler for all PyramidHTTP controllers """

    def __init__(self, namespace, view):
        """ Initialize the handler

        :param namespace: registry nae of the controller
        :param view: route name of the view
        """
        self.namespace = namespace
        self.view = view

    def wrap_view(self, request):
        """ Call and return the result of wanted controller

        :param request: http request got from pyramid
        """
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
    """ Handler for all PyramidRPC controllers """

    def __init__(self, namespace, method):
        """ Initialize the handler

        :param namespace: registry nae of the controller
        :param method: rpc method name of the controller
        """
        self.namespace = namespace
        self.method = method

    def wrap_view(self, request, *args, **kwargs):
        """ Call and return the result of wanted controller

        :param request: http request got from pyramid
        :param \*args: list of argument for rpc method
        :param \*\*kwargs: list of positional argument for rpc method
        """
        self.init_controller(request)
        self.function = self.controller.get_function_from_method(self.method)
        self.controller.check_function(self.function)
        return self.call_controller(*args, **kwargs)
