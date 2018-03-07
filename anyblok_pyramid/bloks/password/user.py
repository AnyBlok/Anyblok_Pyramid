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


@Declarations.register(Declarations.Model.User)
class CredentialStore:
    """Save in table login / password"""
    login = String(
        primary_key=True, nullable=False,
        foreign_key=Declarations.Model.User.use('login').options(
            ondelete='cascade')
    )
    password = Password(
        nullable=False, crypt_context={'schemes': ['md5_crypt']})


@Declarations.register(Declarations.Model)
class User:

    @classmethod
    def check_login(cls, login=None, password=None, **kwargs):
        """Overwrite the method to check if the user exist and
        the password gave is the same sa the password stored

        :param login: str
        :param password: str
        :exception: HTTPUnauthorized
        """
        Credential = cls.registry.User.CredentialStore
        credential = Credential.query().filter(
            Credential.login == login
        ).one_or_none()
        if credential:
            if credential.password == password:
                return login

        raise HTTPUnauthorized(comment="Login or Password invalid")
