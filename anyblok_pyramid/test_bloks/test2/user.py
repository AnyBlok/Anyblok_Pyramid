# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from pyramid.security import Allow, Authenticated


@Declarations.register(Declarations.Model.Pyramid)
class User:

    @classmethod
    def check_login(cls, login=None, password=None):
        return login

    @classmethod
    def get_acl(cls, login, resource, **params):
        return [
            (Allow, Authenticated, 'read'),
            (Allow, 'admin', 'write'),
        ]


@Declarations.register(Declarations.Model)
class Pyramid:
    @classmethod
    def check_user_exists(cls, login):
        if login == "user@anyblok.org":
            return
        raise ValueError("Unknown user")
