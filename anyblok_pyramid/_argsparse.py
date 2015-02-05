# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok._argsparse import ArgsParseManager


@ArgsParseManager.add('wsgi')
def define_wsgi_option(parser, configuration):
    parser.add_argument('--databases', dest='dbnames', default='',
                        help='List of the database allow to be load')
