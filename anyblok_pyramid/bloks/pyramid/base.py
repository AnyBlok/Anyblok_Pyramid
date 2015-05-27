# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from .exceptions import (PyramidInvalidFunction, PyramidInvalidView,
                         PyramidInvalidMethod, PyramidInvalidProperty)
register = Declarations.register
Core = Declarations.Core


@register(Core)
class PyramidBase:

    def __init__(self, request):
        self.request = request
        self.session = request.session

    def check_function(self, function):
        if not hasattr(self, function):
            raise PyramidInvalidFunction("%s has no %s function" % (
                self.__registry_name__, function))

        if function in self.properties:
            for k, v in self.properties[function].items():
                func = 'check_property_%s' % k
                if not hasattr(self, func):
                    raise PyramidInvalidProperty('%s has no %s function' % (
                        self.__registry_name__, func))

                getattr(self, func)(v)

    def check_property_authentificated(self, value):
        return True


@register(Core)
class PyramidBaseHTTP:

    def get_function_from_view(self, view):
        if view not in self.views:
            raise PyramidInvalidView('%s has no %s view' % (
                self.__registry_name__, view))

        return self.views[view]


@register(Core)
class PyramidBaseRPC:

    def get_function_from_method(self, method):
        if method not in self.rpc_methods:
            raise PyramidInvalidMethod('%s has no %s method' % (
                self.__registry_name__, method))

        return self.rpc_methods[method]
