# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from anyblok import Declarations
from anyblok.column import String
from anyblok.field import Function
from pyramid.security import Allow, ALL_PERMISSIONS


@Declarations.register(Declarations.Model)
class User:
    """User declaration need for Auth"""

    login = String(primary_key=True, nullable=False)
    first_name = String(nullable=False)
    last_name = String(nullable=False)
    name = Function(fget='get_name')

    def get_name(self):
        """Return the name of the user"""
        return self.first_name + ' ' + self.last_name.upper()

    @classmethod
    def get_roles(cls, login):
        """Return the roles of an user

        :param login: str, login attribute of the user
        :rtype: list of str (name of the roles)
        """
        # cache the method
        roles = [login]
        user = cls.query().filter(cls.login == login).one_or_none()
        if user:
            for role in user.roles:
                roles.extend(role.roles_name)

        return list(set(roles))

    @classmethod
    def get_acl(cls, login, resource, params=None):
        """Retun the ACL for a ressource and a user

        Auth, does not implement any rule to compute ACL,
        This method allow all user to use the resource ask
        by controllers.

        For other configuration, this method must be overwrite

        :param login: str, login attribute of the user
        :param resource: str, name of a resource
        :param params: all options need to compute ACL
        """
        # cache the method
        return [(Allow, login, ALL_PERMISSIONS)]

    @classmethod
    def format_login_params(cls, request):
        """Return the login and password from query

        By default the query come from json_body and are named
        **login** and **password**

        If the entries come from another place, this method must be overwrite
        :param request: the request from the controllers
        """
        return request.json_body

    @classmethod
    def check_login(cls, login=None, password=None, **kwargs):
        """Check login / password

        This method raise an exception, because any credential
        is stored in this bloks

        .. warning::

            This method must be overwriting by anycredential blok


        :param login: str, the login attribute of the user
        :param password: str
        :param kwargs: any options need to validate credential
        """
        raise HTTPUnauthorized()

    @classmethod
    def get_login_location_to(cls, login, request):
        """Return the default path after the login"""
        return '/'

    @classmethod
    def get_logout_location_to(cls, request):
        """Return the default path after the logout"""
        return '/'
