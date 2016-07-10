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
from logging import getLogger

logger = getLogger(__name__)


def get_registry_for(dbname):
    settings = {
        'sa.session.extension': AnyBlokZopeTransactionExtension,
    }
    return RegistryManager.get(dbname, **settings)


def preload_databases():
    dbnames = Configuration.get('db_names') or []
    dbname = Configuration.get('db_name')
    Registry = Configuration.get('Registry')
    if dbname not in dbnames:
        dbnames.append(dbname)

    # preload all db names
    dbnames = [x for x in dbnames if x]
    logger.info("Preload the databases : %s", ', '.join(dbnames))
    for dbname in dbnames:
        logger.info("Preload the database : %r", dbname)
        if Registry.db_exists(db_name=dbname):
            registry = get_registry_for(dbname)
            registry.commit()
            registry.session.close()
            logger.info("The database %r is preloaded", dbname)
        else:
            logger.warn("The database %r does not exist", dbname)
