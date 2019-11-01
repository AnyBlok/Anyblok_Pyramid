# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#    Copyright (C) 2019 Alexis TOURNEUX <tourneuxalexis@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok


class UserIdentity(Blok):
    version = "0.1.0"
    author = "Jean-Sébastien Suzanne, Alexis Tourneux"
    required = ['anyblok-core', 'auth']

    @classmethod
    def import_declaration_module(cls):
        from . import user  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import user
        reload(user)
