# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_pyramid.security import AnyBlokResourceFactory


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
        config.scan(cls.__module__ + '.views')
