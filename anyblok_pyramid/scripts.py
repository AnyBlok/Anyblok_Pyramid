# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from wsgiref.simple_server import make_server
from anyblok.blok import BlokManager
from anyblok.scripts import format_configuration
from anyblok.config import Configuration
from .pyramid_config import Configurator
import sys
from anyblok import load_init_function_from_entry_points
from .common import preload_databases
from logging import getLogger
logger = getLogger(__name__)


def anyblok_wsgi(application, configuration_groups, **kwargs):
    """
    :param application: name of the application
    :param configuration_groups: list configuration groupe to load
    :param \**kwargs: ArgumentParser named arguments
    """
    format_configuration(configuration_groups, 'preload', 'pyramid-debug',
                         'wsgi')
    load_init_function_from_entry_points()
    Configuration.load(application,
                       configuration_groups=configuration_groups, **kwargs)
    BlokManager.load()
    config = Configurator()
    config.include_from_entry_point()
    config.load_config_bloks()

    wsgi_host = Configuration.get('wsgi_host')
    wsgi_port = int(Configuration.get('wsgi_port'))

    app = config.make_wsgi_app()
    server = make_server(wsgi_host, wsgi_port, app)
    preload_databases()

    logger.info("Serve forever on %r:%r" % (wsgi_host, wsgi_port))
    server.serve_forever()


def wsgi():
    anyblok_wsgi('pyramid', ['logging'])


def gunicorn_anyblok_wsgi(application, configuration_groups, **kwargs):
    try:
        import gunicorn  # noqa
    except ImportError:
        logger.error("No gunicorn installed")
        sys.exit(1)

    format_configuration(configuration_groups, 'preload', 'pyramid-debug')
    from .gunicorn import WSGIApplication
    WSGIApplication(application,
                    configuration_groups=configuration_groups).run()


def gunicorn_wsgi():
    gunicorn_anyblok_wsgi('gunicorn', ['logging'])
