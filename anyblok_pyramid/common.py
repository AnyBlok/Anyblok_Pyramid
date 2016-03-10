# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration
from .anyblok import AnyBlokZopeTransactionExtension
from anyblok.registry import RegistryManager


def preload_databases():
    dbnames = Configuration.get('db_names', '').split(',')
    dbname = Configuration.get('db_name')
    if dbname not in dbnames:
        dbnames.append(dbname)

    # preload all db names
    settings = {
        'sa.session.extension': AnyBlokZopeTransactionExtension,
    }
    for dbname in [x for x in dbnames if x != '']:
        registry = RegistryManager.get(dbname, **settings)
        registry.commit()
        registry.session.close()
