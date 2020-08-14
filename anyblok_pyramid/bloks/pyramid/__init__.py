# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2020 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from pyramid.authorization import ACLAuthorizationPolicy
from anyblok_pyramid.security import RootFactory
from .pyramid import getAuthenticationPolicy


def declarations(reload=None):
    from . import model
    if reload:
        reload(model)


class Pyramid(Blok):
    version = "0.1.0"
    author = "Jean-Sébastien Suzanne"
    required = ['anyblok-core']

    @classmethod
    def import_declaration_module(cls):
        declarations()

    @classmethod
    def reload_declaration_module(cls, reload):
        declarations(reload=reload)

    @classmethod
    def pyramid_load_config(cls, config):
        # get authentication on view
        authn_policy = getAuthenticationPolicy()
        config.set_authentication_policy(authn_policy)
        # get autorization
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
        config.set_root_factory(RootFactory)
