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

    login = String(primary_key=True, nullable=False)
    first_name = String(nullable=False)
    last_name = String(nullable=False)
    name = Function(fget='get_name')

    def get_name(self):
        return self.first_name + ' ' + self.last_name.upper()

    @classmethod
    def get_roles(cls, login):
        # cache the method
        roles = [login]
        user = cls.query().filter(cls.login == login).one_or_none()
        if user:
            for role in user.roles:
                roles.extend(role.roles_name)

        return list(set(roles))

    @classmethod
    def get_acl(cls, login, resource, **params):
        # cache the method
        return [(Allow, login, ALL_PERMISSIONS)]

    @classmethod
    def format_login_params(cls, request):
        return request.json_body

    @classmethod
    def check_login(cls, login=None, password=None, **kwargs):
        raise HTTPUnauthorized()

    @classmethod
    def get_login_location_to(cls, login, request):
        return '/'

    @classmethod
    def get_logout_location_to(cls, request):
        return '/'
