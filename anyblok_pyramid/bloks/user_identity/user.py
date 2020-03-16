# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2019 Alexis TOURNEUX <tourneuxalexis@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import String
from anyblok.field import Function


@Declarations.register(Declarations.Model.Pyramid)
class User:
    """User declaration for identity"""

    first_name = String(nullable=False)
    last_name = String(nullable=False)
    name = Function(fget='get_name')

    def get_name(self):
        """Return the name of the user"""
        return self.first_name + ' ' + self.last_name.upper()
