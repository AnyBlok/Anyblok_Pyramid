# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.declarations import classmethod_cache
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

    @classmethod
    def _get_user(cls, user_id):
        """Return user for a given `user_id`, to be overwrite in user bloks
        The method is called by `get_user` cached method to retreive user
        while restricting query by user.

        .. warning::

            User cache invalidation must be done by developer.

        :param user_id: This is the user primary key (could be a loging
            according the User class definition)
        :return User (instance ?) or None: retreive the user for the given
            `user_id`
        """
        return user_id

    @classmethod_cache()
    def get_user(cls, user_id):
        """Cached `_get_user` results in order to use it by
        ``restrict_query_by_user`` decorators. Invalidate
        cache has to be implemented by user who use it"""
        return cls._get_user(user_id)

    @classmethod
    def restrict_query_by_user(
        cls, query, user_code
    ):
        """Call registered decorated method (by
        ``from anyblok_pyramid.bloks.pyramid.restrict.restrict_query_by_user``)
        to add filters on current query according the selected model.

        :param query: A query object which you have to add filters
        :user_code: User primary key value used to retreive users.

        .. note::

            This method is using get_user which cached user instance, you
            have to manage or mind to cache invalidation while using this
            method.
        """
        for method in cls.registry.restrict_query_by_user_methods.get(
            query.Model, []
        ):

            query = getattr(
                cls.registry.get(query.Model), method
            )(query, cls.get_user(user_code))

        return query
