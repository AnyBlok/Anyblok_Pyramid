# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import BlokManager
from .common import preload_databases
import sys
from anyblok_pyramid.pyramid_config import Configurator
from anyblok.config import Configuration
from os import environ, path
from appdirs import AppDirs
from anyblok import load_init_function_from_entry_points

if BlokManager.bloks:
    # AnyBlok already load, the state are not sure, better to stop here
    sys.exit(1)


load_init_function_from_entry_points()
# load default files
ad = AppDirs('AnyBlok')
# load the global configuration file
Configuration.parse_configfile(path.join(ad.site_config_dir, 'conf.cfg'), ())
# load the user configuration file
Configuration.parse_configfile(path.join(ad.user_config_dir, 'conf.cfg'), ())
# load config file in environment variable
configfile = environ.get('ANYBLOK_CONFIGFILE')
if configfile:
    Configuration.parse_configfile(configfile, ())

if 'logging_level' in Configuration.configuration:
    Configuration.initialize_logging()

BlokManager.load()
preload_databases()
config = Configurator()
config.include_from_entry_point()
config.load_config_bloks()
app = config.make_wsgi_app()
