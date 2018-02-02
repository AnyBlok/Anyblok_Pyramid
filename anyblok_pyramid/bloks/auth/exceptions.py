# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.common import python_version

if python_version() >= (3, 5):
    MainException = RecursionError  # noqa
else:
    MainException = RuntimeError


class RecursionRoleError(MainException):
    """Simple exception to check if the roles is cyclic"""
