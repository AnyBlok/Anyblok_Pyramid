# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration, AnyBlokPlugin
from .release import version
import os


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


def get_db_name(request):
    return Configuration.get('db_name')


@Configuration.add('preload', label="Preload")
def define_preload_option(group):
    group.add_argument('--databases', dest='db_names', nargs="+",
                       help='List of the database allow to be load')


@Configuration.add('wsgi', label="WSGI")
def define_wsgi_option(group):
    group.add_argument(
        '--wsgi-host',
        default=os.environ.get('ANYBLOK_PYRAMID_WSGI_HOST', 'localhost'))
    group.add_argument(
        '--wsgi-port', type=int,
        default=os.environ.get('ANYBLOK_PYRAMID_WSGI_PORT', 5000))


@Configuration.add('pyramid-debug', label="Pyramid")
def define_wsgi_debug_option(group):
    group.add_argument('--pyramid-reload-all', dest='pyramid.reload_all',
                       help="Turns on all reload* settings.",
                       action='store_true')
    group.add_argument('--pyramid-reload-templates',
                       dest='pyramid.reload_templates',
                       help="templates are "
                            "automatically reloaded whenever they are "
                            "modified without restarting the application, so "
                            "you can see changes to templates take effect "
                            "immediately during development. This flag is "
                            "meaningful to Chameleon and Mako templates, as "
                            "well as most third-party template rendering "
                            "extensions.",
                       action='store_true')
    group.add_argument('--pyramid-reload-assets',
                       dest='pyramid.reload_assets',
                       help="Don't cache any asset file data",
                       action='store_true')
    group.add_argument('--pyramid-debug-all',
                       dest='pyramid.debug_all',
                       help="Turns on all debug* settings.",
                       action='store_true')
    group.add_argument('--pyramid-debug-notfound',
                       dest='pyramid.debug_notfound',
                       help="Print view-related NotFound debug messages "
                            "to stderr",
                       action='store_true')
    group.add_argument('--pyramid-debug-routematch',
                       dest='pyramid.debug_routematch',
                       help="Print debugging messages related to url dispatch "
                            "route matching",
                       action='store_true')
    group.add_argument('--pyramid-prevent-http-cache',
                       dest='pyramid.prevent_http_cache',
                       help="Prevent the http_cache view configuration "
                            "argument from having any effect globally in this "
                            "process when this value is true. No http "
                            "caching-related response headers will be set by "
                            "the Pyramid http_cache view configuration "
                            "feature",
                       action='store_true')
    group.add_argument('--pyramid-default-locale-name',
                       dest='pyramid.default_locale_name',
                       help="The value supplied here is used as the default "
                            "locale name when a locale negotiator is not "
                            "registered.",
                       default='')


@Configuration.add('gunicorn')
def add_configuration_file(parser):
    parser.add_argument('--anyblok-configfile', dest='configfile', default='',
                        help="Relative path of the config file")
    parser.add_argument('--without-auto-migration',
                        dest='withoutautomigration',
                        action='store_true')


@Configuration.add('plugins')
def update_plugins(group):
    group.add_argument('--get-db-name-plugin',
                       dest='get_db_name', type=AnyBlokPlugin,
                       default='anyblok_pyramid.config:get_db_name',
                       help="get_db_name function to use")
