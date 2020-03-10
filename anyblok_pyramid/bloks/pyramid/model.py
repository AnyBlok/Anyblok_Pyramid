# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from anyblok import Declarations
from pyramid.security import Allow, ALL_PERMISSIONS


@Declarations.register(Declarations.Model)
class Pyramid:

    @classmethod
    def get_roles(cls, login):
        """Return the roles of an user

        This method must be ober writting by the auth blok

        :param login: str, login attribute of the user
        :rtype: list of str (name of the roles)
        """
        return []

    @classmethod
    def get_acl(cls, login, resource, params=None):
        """Retun the ACL for a ressource and a user

        Auth, does not implement any rule to compute ACL,
        This method allow all user to use the resource ask
        by controllers.

        For other configuration, this method must be overwrite

        This method must be ober writting by the auth blok

        :param login: str, login attribute of the user
        :param resource: str, name of a resource
        :param params: all options need to compute ACL
        """
        # cache the method
        return [(Allow, login, ALL_PERMISSIONS)]

    @classmethod
    def check_acl(cls, login, resource, type_):
        """Retun True if user is allowed to make action type
        of the resource

        This method must be ober writting by the auth blok

        :param login: str, login attribute of the user
        :param resource: str, name of a resource
        :param type: str, name of the action
        :param params: all options need to compute ACL
        """
        # cache the method
        return True

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
    def check_login(cls, **kwargs):
        """Check login / password

        This method raise an exception, because any credential
        is stored in this bloks

        .. warning::

            This method must be overwriting by anycredential blok


        :param kwargs: any options need to validate credential
        """
        raise HTTPUnauthorized()

    @classmethod
    def check_user_exists(cls, login):
        raise NotImplementedError()
