# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from anyblok import Declarations
from anyblok.column import String
from pyramid.security import Allow, ALL_PERMISSIONS


@Declarations.register(Declarations.Model)
class Pyramid:

    @classmethod
    def get_roles(cls, login):
        """Return the roles of an user

        :param login: str, login attribute of the user
        :rtype: list of str (name of the roles)
        """
        return cls.registry.Pyramid.User.get_roles(login)

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
        return cls.registry.Pyramid.User.get_acl(
            login, resource, params=params)

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
        return cls.registry.Pyramid.User.check_acl(
            login, resource, type_)

    @classmethod
    def check_login(cls, **kwargs):
        """Check login / password

        This method raise an exception, because any credential
        is stored in this bloks

        .. warning::

            This method must be overwriting by anycredential blok


        :param kwargs: any options need to validate credential
        """
        return cls.registry.Pyramid.User.check_login(**kwargs)

    @classmethod
    def check_user_exists(cls, login):
        user = cls.registry.Pyramid.User.query().get(login)
        if user is None:
            raise KeyError('%s is not a valid login')

        return user

    @classmethod
    def _get_user(cls, user_id):
        """Return user for a given user_id.
        The method is called by `Model.Pyramid.get_user` cached method
        to retreive user. You (as developer) must implement a cache
        invalidation in case of user modification that could impact
        restricted query by user id
        """
        return cls.registry.Pyramid.User.query().get(user_id)


@Declarations.register(Declarations.Model.Pyramid)
class User:
    """User declaration need for Auth"""

    login = String(primary_key=True, nullable=False)

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
    def check_acl(cls, login, resource, type_):
        """Overwrite the method to return the ACL for the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        :param type: str, name of the action
        """
        return True

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
