# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from wsgiref.simple_server import make_server
from anyblok.blok import BlokManager
from anyblok.config import Configuration
from .pyramid_config import Configurator
import sys
from anyblok import (
    load_init_function_from_entry_points,
    configuration_post_load,
)
from .common import preload_databases
from colorama import Fore, Style
from logging import getLogger
logger = getLogger(__name__)


def wsgi():
    """Simple Pyramid wsgi server for development purpose
    """
    load_init_function_from_entry_points()
    Configuration.load('pyramid')
    configuration_post_load()
    BlokManager.load()
    config = Configurator()
    config.include_from_entry_point()
    config.load_config_bloks()

    wsgi_host = Configuration.get('wsgi_host')
    wsgi_port = int(Configuration.get('wsgi_port'))

    app = config.make_wsgi_app()
    server = make_server(wsgi_host, wsgi_port, app)
    preload_databases(loadwithoutmigration=False)

    start_msg = f"Pyramid development server running at "\
                f"{Fore.BLUE}http://{wsgi_host}:{wsgi_port}{Style.RESET_ALL}"
    logger.info(start_msg)
    print(start_msg)
    server.serve_forever()


def gunicorn_wsgi():
    """console script function to run anyblok / pyramid with gunicorn"""
    try:
        import gunicorn  # noqa
    except ImportError:
        logger.error("Gunicorn is not installed. Try: pip install gunicorn")
        sys.exit(1)

    from .gunicorn import WSGIApplication
    WSGIApplication('gunicorn').run()
