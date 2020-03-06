# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from anyblok import Declarations
from anyblok.column import String, Password


@Declarations.register(Declarations.Model.Pyramid)
class CredentialStore:
    """Simple login / password table"""
    login = String(
        primary_key=True, nullable=False,
        foreign_key=Declarations.Model.Pyramid.User.use('login').options(
            ondelete='cascade')
    )
    password = Password(
        nullable=False, crypt_context={'schemes': ['md5_crypt']})


@Declarations.register(Declarations.Model.Pyramid)
class User:

    @classmethod
    def check_login(cls, login=None, password=None, **kwargs):
        """Overwrite the initial method to check if the given login match with
        an existing user that has the same password.

        :param login: str
        :param password: str
        :exception: HTTPUnauthorized
        """
        Credential = cls.registry.Pyramid.CredentialStore
        credential = Credential.query().filter(
            Credential.login == login
        ).one_or_none()
        if credential:
            if credential.password == password:
                return login

        raise HTTPUnauthorized(comment="Login or Password invalid")
