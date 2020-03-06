# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2020 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok


def declarations(reload=None):
    from . import user
    from . import role
    if reload:
        reload(user)
        reload(role)


class Auth(Blok):
    version = "0.1.0"
    author = "Jean-Sébastien Suzanne"
    required = ['anyblok-core', 'pyramid']

    @classmethod
    def import_declaration_module(cls):
        declarations()

    @classmethod
    def reload_declaration_module(cls, reload):
        declarations(reload=reload)
