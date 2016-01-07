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


def load_init_function_from_entry_points():
    """Call all the entry point ``anyblok_pyramid.init`` to update
    the argument setting

    the callable need to have one parametter, it is a dict::

        def init_function():
            ...

    We add the entry point by the setup file::

        setup(
            ...,
            entry_points={
                'anyblok_pyramid.init': [
                    init_function=path:init_function,
                    ...
                ],
            },
            ...,
        )


    """
    from pkg_resources import iter_entry_points
    for i in iter_entry_points('anyblok_pyramid.init'):
        logger.debug('Load init: %r' % i.name)
        i.load()()
