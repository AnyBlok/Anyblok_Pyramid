# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from pyramid.security import remember, forget
from logging import getLogger

logger = getLogger(__name__)


def login(request):
    """Default view to login a user"""
    Pyramid = request.anyblok.registry.Pyramid
    params = Pyramid.format_login_params(request)
    if Pyramid.check_login(**params):
        login = params['login']
        headers = remember(request, login)
        logger.info('%s is logged in', login)
        location = Pyramid.User.get_login_location_to(login, request)
        return HTTPFound(location=location, headers=headers)

    return HTTPUnauthorized(comment='Login failed')


def logout(request):
    """Default view to logout a user"""
    logger.info('%r is logged out', request.authenticated_userid)
    headers = forget(request)
    User = request.anyblok.registry.Pyramid.User
    location = User.get_logout_location_to(request)
    return HTTPFound(location=location, headers=headers)
