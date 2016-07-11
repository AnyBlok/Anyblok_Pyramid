# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import BlokManager
import inspect


def anyblok_init_config(unittest=False):
    from anyblok import config  # noqa import anyblok.config
    from . import config  # noqa import config definition


class AnyBlokPyramidException(Exception):
    pass


def current_blok():
    filename = inspect.stack()[1][1]
    for blok in BlokManager.ordered_bloks:
        if filename.startswith(BlokManager.getPath(blok)):
            return blok

    raise AnyBlokPyramidException("You are not in a Blok")
