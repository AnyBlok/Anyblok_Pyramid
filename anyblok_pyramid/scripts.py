# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from wsgiref.simple_server import make_server
from anyblok.scripts import format_argsparse
from anyblok.registry import RegistryManager
from anyblok._argsparse import ArgsParseManager
from .config import make_config


def anyblok_wsgi(description, version, argsparse_groups,
                 Configurator=make_config):
    """
    :param description: description of argsparse
    :param version: version of script for argparse
    :param argsparse_groups: list argsparse groupe to load
    :param Configurator: callable which return a config instance
    """
    format_argsparse(argsparse_groups, 'wsgi', 'pyramid-debug', 'beaker')
    ArgsParseManager.load(description="%s (%s)" % (description, version),
                          argsparse_groups=argsparse_groups)
    RegistryManager.add_needed_bloks('pyramid')
    config = Configurator()
    wsgi_host = ArgsParseManager.get('wsgi_host')
    wsgi_port = int(ArgsParseManager.get('wsgi_port'))

    app = config.make_wsgi_app()
    server = make_server(wsgi_host, wsgi_port, app)

    dbnames = ArgsParseManager.get('dbnames', '').split(',')
    dbname = ArgsParseManager.get('dbname')
    if dbname not in dbnames:
        dbnames.append(dbname)

    # preload all db names
    for dbname in [x for x in dbnames if x != '']:
        RegistryManager.get(dbname)

    server.serve_forever()


def wsgi():
    anyblok_wsgi('Web server for AnyBlok', '0.0.1',
                 ['config', 'database'])
