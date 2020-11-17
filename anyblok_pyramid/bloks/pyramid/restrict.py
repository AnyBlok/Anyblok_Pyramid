# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2002 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.common import add_autodocs
from anyblok.model.plugins import ModelPluginBase


class RestrictQueryByUserIdPlugin(ModelPluginBase):
    """An AnyBlok plugin that helps to add extra filters on queries according
    the current user"""

    def __init__(self, registry):
        if not hasattr(registry, "restrict_query_by_user_methods"):
            registry.restrict_query_by_user_methods = {}

        super().__init__(registry)

    def transform_base_attribute(
        self, attr, method, namespace, base, transformation_properties,
        new_type_properties,
    ):
        """Find restricted methods in the base to save the
        namespace and the method in the registry
        :param attr: attribute name
        :param method: method pointer of the attribute
        :param namespace: the namespace of the model
        :param base: One of the base of the model
        :param transformation_properties: the properties of the model
        :param new_type_properties: param to add in a new base if need
        """
        if (
            hasattr(method, "is_a_restric_query_by_user_method")
            and method.is_a_restric_query_by_user_method is True
        ):
            if namespace not in self.registry.restrict_query_by_user_methods:
                self.registry.restrict_query_by_user_methods[namespace] = {}
            self.registry.restrict_query_by_user_methods[namespace].update(
                {method.__name__: method}
            )


def restrict_query_by_user():
    autodoc = """Decorator to register a class method to restrict query
    by user. Decorated class method will receive a query object and a user
    instance, developer must return a query object with additionnal filters::

        from anyblok_pyramid.bloks.pyramid.restrict import (
            restrict_query_by_user
        )
        ...
            @restrict_query_by_user()
            def restrict_reading_this_blok_to_user2(cls, query, user):
                if user.login == "user2@anyblok.org":
                    query = query.filter_by(name="test-pyramid2")
                return query
    """

    def wrapper(method):
        add_autodocs(method, autodoc)
        method.is_a_restric_query_by_user_method = True
        return classmethod(method)

    return wrapper
