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
from .config import make_config


def anyblok_wsgi(description, version, configuration_groups,
                 Configurator=make_config):
    """
    :param description: description of configuration
    :param version: version of script for argparse
    :param configuration_groups: list configuration groupe to load
    :param Configurator: callable which return a config instance
    """
    format_configuration(configuration_groups, 'wsgi', 'pyramid-debug',
                         'beaker')
    BlokManager.load()
    Configuration.load(description="%s (%s)" % (description, version),
                       configuration_groups=configuration_groups)
    RegistryManager.add_needed_bloks('pyramid')
    config = Configurator()
    wsgi_host = Configuration.get('wsgi_host')
    wsgi_port = int(Configuration.get('wsgi_port'))

    app = config.make_wsgi_app()
    server = make_server(wsgi_host, wsgi_port, app)

    dbnames = Configuration.get('db_names', '').split(',')
    dbname = Configuration.get('db_name')
    if dbname not in dbnames:
        dbnames.append(dbname)

    # preload all db names
    for dbname in [x for x in dbnames if x != '']:
        RegistryManager.get(dbname)

    server.serve_forever()


def wsgi():
    anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                 ['config', 'database'])
