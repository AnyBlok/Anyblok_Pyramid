# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from pyramid.authorization import ACLAuthorizationPolicy
from anyblok_pyramid.security import RootFactory
from .pyramid import getAuthenticationPolicy


class Auth(Blok):
    version = "0.1.0"
    author = "Jean-Sébastien Suzanne"
    required = ['anyblok-core']

    @classmethod
    def import_declaration_module(cls):
        from . import user  # noqa
        from . import role  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import user
        reload(user)
        from . import role
        reload(role)

    @classmethod
    def pyramid_load_config(cls, config):
        # get authentication on view
        authn_policy = getAuthenticationPolicy()
        config.set_authentication_policy(authn_policy)
        # get autorization
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
        config.set_root_factory(RootFactory)
