# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_pyramid.release import version


class Pyramid(Blok):
    """
    Server tools to use the Pyramid views and routes declarations with
    the AnyBlok framework
    """
    version = version

    required = [
        'anyblok-core',
    ]

    @classmethod
    def import_declaration_module(cls):
        from . import base  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import base
        reload(base)
