# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from . import config  # noqa
from . import controllers  # noqa
from logging import getLogger
logger = getLogger(__name__)

callables = {}


def set_callable(c):
    callables[c.__name__] = c


def get_callable(k):
    return callables[k]


from . import handler  # noqa
