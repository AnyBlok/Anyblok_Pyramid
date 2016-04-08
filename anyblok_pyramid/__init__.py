# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .release import version
from anyblok.config import Configuration


callables = {}


def set_callable(c):
    callables[c.__name__] = c
    return c


def get_callable(k):
    return callables[k]


def anyblok_init_config():
    from . import config  # noqa import config definition
    Configuration.applications.update({
        'pyramid': {
            'prog': 'AnyBlok simple wsgi app, version %r' % version,
            'description': "WSGI for test your AnyBlok / Pyramid app",
            'configuration_groups': ['config', 'database'],
        },
        'gunicorn': {
            'prog': 'AnyBlok gunicorn wsgi app, version %r' % version,
            'description': "GUNICORN for test your AnyBlok / Pyramid app",
            'configuration_groups': ['gunicorn', 'database'],
        },
    })


@set_callable
def get_db_name(request):
    return Configuration.get('db_name')
