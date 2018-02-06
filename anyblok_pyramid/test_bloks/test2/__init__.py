# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_pyramid.security import AnyBlokResourceFactory
from anyblok_pyramid.bloks.auth.views import login, logout


class Test(Blok):

    version = '1.0.0'
    required = ['auth']

    @classmethod
    def import_declaration_module(cls):
        from . import user  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import user
        reload(user)

    @classmethod
    def pyramid_load_config(cls, config):
        config.add_route('bloks', '/bloks',
                         factory=AnyBlokResourceFactory('Model.System.Blok'))
        config.add_route('blok', '/blok/{name}',
                         factory=AnyBlokResourceFactory('Model.System.Blok'))
        config.add_route('login', '/login', request_method='POST')
        config.add_view(view=login, route_name='login', renderer="JSON")
        config.add_route('logout', '/logout', request_method='POST')
        config.add_view(view=logout, route_name='logout')
        config.scan(cls.__module__ + '.views')
