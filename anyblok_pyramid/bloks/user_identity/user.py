# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.httpexceptions import HTTPUnauthorized
from anyblok import Declarations
from anyblok.column import String
from anyblok.field import Function
from pyramid.security import Allow, ALL_PERMISSIONS


@Declarations.register(Declarations.Model)
class User:
    """User declaration for identity"""

    first_name = String(nullable=False)
    last_name = String(nullable=False)
    name = Function(fget='get_name')

    def get_name(self):
        """Return the name of the user"""
        return self.first_name + ' ' + self.last_name.upper()
