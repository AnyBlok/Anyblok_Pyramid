# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.view import view_defaults, view_config
from anyblok_pyramid import current_blok
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from pyramid.security import remember, forget
from logging import getLogger

logger = getLogger(__name__)


@view_defaults(installed_blok=current_blok())
class Auth:

    def __init__(self, request):
        self.request = request
        self.User = request.anyblok.registry.User

    @view_config(route_name='login')
    def login(self):
        params = self.User.format_login_params(**dict(self.request.params))
        if self.User.check_login(**params):
            login = params['login']
            headers = remember(self.request, login)
            logger.info('%s is logged in', login)
            location = self.User.get_login_location_to(login, self.request)
            return HTTPFound(location=location, headers=headers)

        return HTTPUnauthorized(comment='Login failed')

    @view_config(route_name='logout')
    def logout(self):
        logger.info('%r is logged out', self.request.authenticated_userid)
        headers = forget(self.request)
        location = self.User.get_logout_location_to(self.request)
        return HTTPFound(location=location, headers=headers)
