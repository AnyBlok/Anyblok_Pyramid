# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration, AnyBlokPlugin, get_db_name as gdb
from .release import version
import os

Configuration.add_application_properties(
    'pyramid', ['logging', 'pyramid-debug', 'wsgi', 'auth', 'preload'],
    prog='AnyBlok simple wsgi app, version %r' % version,
    description="WSGI for test your AnyBlok / Pyramid app",
)

Configuration.add_application_properties(
    'gunicorn', [],
    prog='AnyBlok simple wsgi app, version %r' % version,
    description="WSGI for test your AnyBlok / Pyramid app",
    configuration_groups=['logging', 'pyramid-debug', 'auth', 'preload',
                          'gunicorn', 'database'],
)
Configuration.add_application_properties('nose', ['auth'])


def get_db_name(request):
    return gdb()


@Configuration.add('wsgi', label="WSGI")
def define_wsgi_option(group):
    group.add_argument(
        '--wsgi-host',
        default=os.environ.get('ANYBLOK_PYRAMID_WSGI_HOST', 'localhost'))
    group.add_argument(
        '--wsgi-port', type=int,
        default=os.environ.get('ANYBLOK_PYRAMID_WSGI_PORT', 5000))


@Configuration.add('auth', label="Authentication and Authorization",
                   must_be_loaded_by_unittest=True)
def define_auth_option(group):
    group.add_argument(
        '--pyramid-authentication-method', type=AnyBlokPlugin,
        default='pyramid.authentication:AuthTktAuthenticationPolicy',
        help="authentication function to use")
    group.add_argument(
        '--pyramid-authentication-debug',
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHENTICATION_DEBUG', False),
        help=(
            "If debug is True, log messages to the Pyramid debug logger about "
            "the results of various authentication stepsn"
        ),
        action='store_true')
    group.add_argument(
        '--pyramid-authentication-callback', type=AnyBlokPlugin,
        default='anyblok_pyramid.security:group_finder',
        help=(
            "A callback passed the userid and the request, expected to return "
            "None if the userid doesn’t exist or a sequence of principal "
            "identifiers (possibly empty) if the user does exist. If callback "
            "is None, the userid will be assumed to exist with no principals"
        ))

    # AuthTktAuthenticationPolicy
    group.add_argument(
        '--pyramid-authtkt-secret',
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHTKT_SECRET', 'secret'),
        help=(
            "The secret (a string) used for auth_tkt cookie signing. This "
            "value should be unique across all values provided to Pyramid "
            "for various subsystem secrets"
        ))
    group.add_argument(
        '--pyramid-authtkt-cookie-name',
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHTKT_COOKIE_NAME',
                               'auth_tkt'),
        help="The cookie name used")
    group.add_argument(
        '--pyramid-authtkt-secure',
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHTKT_SECURE', False),
        help="Only send the cookie back over an unsecure conn",
        action='store_true')
    group.add_argument(
        '--pyramid-authtkt-timeout', type=int,
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHTKT_TIMEOUT', None),
        help=(
            "Maximum number of seconds which a newly issued ticket will be "
            "considered valid. After this amount of time, the ticket will "
            "expire (effectively logging the user out). If this value is None"
            ", the ticket never expires"
        ))
    group.add_argument(
        '--pyramid-authtkt-max-age', type=int,
        default=os.environ.get('ANYBLOK_PYRAMID_AUTHTKT_MAX_AGE', None),
        help=(
            "Maximum number of seconds which a newly issued ticket will be "
            "considered valid. After this amount of time, the ticket will "
            "expire (effectively logging the user out). If this value is None"
            ", the ticket never expires"
        ))

    # RemoteUserAuthenticationPolicy
    group.add_argument(
        '--pyramid-remoteuser-environ-key',
        default=os.environ.get('ANYBLOK_PYRAMID_REMOTEUSER_ENVIRON_KEY',
                               'REMOTE_USER'),
        help="The key in the WSGI environ which provides the userid")

    # SessionAuthenticationPolicy
    group.add_argument(
        '--pyramid-session-prefix',
        default=os.environ.get('ANYBLOK_PYRAMID_SESSION_PREFIX', 'auth'),
        help=(
            "A prefix used when storing the authentication parameters in the "
            "session"
        ))

    # BasicAuthAuthenticationPolicy
    group.add_argument(
        '--pyramid-basicauth-check', type=AnyBlokPlugin,
        default='anyblok_pyramid.security:check_user',
        help=(
            "A callback function passed a username, password and request, in "
            "that order as positional arguments. Expected to return None if "
            "the userid doesn’t exist or a sequence of principal identifiers "
            "(possibly empty) if the user does exist"
        ))


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


@Configuration.add('plugins', must_be_loaded_by_unittest=True)
def update_plugins(group):
    group.add_argument('--get-db-name-plugin',
                       dest='get_db_name', type=AnyBlokPlugin,
                       default='anyblok_pyramid.config:get_db_name',
                       help="get_db_name function to use")
