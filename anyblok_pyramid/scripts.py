# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from wsgiref.simple_server import make_server
from anyblok.blok import BlokManager
from anyblok.scripts import format_configuration
from anyblok.registry import RegistryManager
from anyblok.config import Configuration
from .pyramid_config import Configurator
import sys
from .anyblok import AnyBlokZopeTransactionExtension
from logging import getLogger
logger = getLogger(__name__)


def anyblok_wsgi(application, configuration_groups, **kwargs):
    """
    :param application: name of the application
    :param configuration_groups: list configuration groupe to load
    :param \**kwargs: ArgumentParser named arguments
    """
    format_configuration(configuration_groups, 'preload', 'pyramid-debug',
                         'wsgi', 'beaker')
    Configuration.load(application,
                       configuration_groups=configuration_groups, **kwargs)
    BlokManager.load()
    RegistryManager.add_needed_bloks('pyramid')
    config = Configurator()
    config.include_from_entry_point()

    wsgi_host = Configuration.get('wsgi_host')
    wsgi_port = int(Configuration.get('wsgi_port'))

    app = config.make_wsgi_app()
    server = make_server(wsgi_host, wsgi_port, app)

    dbnames = Configuration.get('db_names', '').split(',')
    dbname = Configuration.get('db_name')
    if dbname not in dbnames:
        dbnames.append(dbname)

    # preload all db names
    settings = {
        'sa.session.extension': AnyBlokZopeTransactionExtension,
    }
    for dbname in [x for x in dbnames if x != '']:
        RegistryManager.get(dbname, **settings).commit()

    logger.info("Serve forever on %r:%r" % (wsgi_host, wsgi_port))
    server.serve_forever()


def wsgi():
    anyblok_wsgi('pyramid', ['logging'])


def gunicorn_anyblok_wsgi(description, version, configuration_groups):
    try:
        import gunicorn  # noqa
    except ImportError:
        logger.error("No gunicorn installed")
        sys.exit(1)

    format_configuration(configuration_groups, 'preload', 'pyramid-debug',
                         'beaker')
    from .gunicorn import WSGIApplication
    WSGIApplication(usage="%s (%s)" % (description, version),
                    configuration_groups=configuration_groups).run()


def gunicorn_wsgi():
    gunicorn_anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                          ['gunicorn', 'database', 'logging'])
