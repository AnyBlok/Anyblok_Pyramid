# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from . import config  # noqa
from . import controllers  # noqa
from .workingset import WorkingSet
from pkg_resources import _call_aside


__all__ = [
    'get_callable',
    'set_callable',
]


@_call_aside
def _initialize_master_working_set():
    ws = WorkingSet._build_master()
    globals().update(dict(set_callable=ws.set_callable,
                          get_callable=ws.get_callable))


from . import handler  # noqa
