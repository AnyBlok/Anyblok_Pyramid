# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok


class Password(Blok):
    version = "0.1.0"
    author = "Jean-Sébastien Suzanne"
    required = ['auth']

    @classmethod
    def import_declaration_module(cls):
        from . import user  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import user
        reload(user)
