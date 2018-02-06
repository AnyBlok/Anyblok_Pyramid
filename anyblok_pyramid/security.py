# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import Deny, Everyone, ALL_PERMISSIONS


def group_finder(userid, request):
    """Return groups from user ID

    :param userid: the user id (login)
    :param request: request from pyramid
    """
    if hasattr(request, 'anyblok') and request.anyblok:
        return request.anyblok.registry.User.get_roles(userid)

    return userid


def check_user(userid, password, request):
    """Return groups from user ID

    :param userid: the user id (login)
    :param request: request from pyramid
    """
    if hasattr(request, 'anyblok') and request.anyblok:
        return request.anyblok.registry.User.check_login(
            login=userid, password=password
        )

    return None


def AnyBlokResourceFactory(resource):

    def __acl__(self):
        if not hasattr(self, 'registry'):
            raise HTTPUnauthorized("ACL have not get AnyBlok registry")

        userid = self.request.authenticated_userid
        if userid:
            return self.registry.User.get_acl(
                userid, self.__resource__,
                **dict(self.request.matchdict)
            )

        return [(Deny, Everyone, ALL_PERMISSIONS)]

    return type('ResourceFactory', (RootFactory,), {
        '__acl__': __acl__,
        '__resource__': resource,
    })


class RootFactory:

    def __init__(self, request):
        self.request = request
        if hasattr(request, 'anyblok'):
            self.registry = request.anyblok.registry
