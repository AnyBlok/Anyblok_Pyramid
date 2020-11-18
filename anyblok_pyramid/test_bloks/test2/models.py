# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2002 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from pyramid.security import Allow, Authenticated
from anyblok_pyramid.bloks.pyramid.restrict import restrict_query_by_user


@Declarations.register(Declarations.Model.Pyramid)
class User:

    @classmethod
    def check_login(cls, login=None, password=None):
        return cls.registry.Pyramid.User.query().get(login)

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
        # if login in ["user@anyblok.org", "user2@anyblok.org"]:
        if login == "user@anyblok.org":
            return
        raise ValueError("Unknown user")


@Declarations.register(Declarations.Model.System)
class Blok:

    @restrict_query_by_user()
    def restrict_reading_this_blok_to_user2(cls, query, user):
        if user.login == "user2@anyblok.org":
            query = query.filter_by(name="test-pyramid2")
        return query
