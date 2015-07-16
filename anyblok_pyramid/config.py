# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration
import os


@Configuration.add('wsgi', label="WSGI")
def define_wsgi_option(group, configuration):
    group.add_argument('--databases', dest='db_names', default='',
                       help='List of the database allow to be load')
    group.add_argument('--wsgi-host', default='')
    group.add_argument('--wsgi-port', default='')
    configuration.update({
        'wsgi_host': os.environ.get('ANYBLOK_PYRAMID_WSGI_HOST', 'localhost'),
        'wsgi_port': os.environ.get('ANYBLOK_PYRAMID_WSGI_PORT', '5000'),
    })


@Configuration.add('pyramid-debug', label="Pyramid")
def define_wsgi_debug_option(group, configuration):
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
    configuration.update({
        'pyramid.reload_all': False,
        'pyramid.reload_templates': False,
        'pyramid.reload_assets': False,
        'pyramid.debug_all': False,
        'pyramid.debug_notfound': False,
        'pyramid.debug_routematch': False,
        'pyramid.prevent_http_cache': False,
        'pyramid.default_locale_name': '',
    })


@Configuration.add('beaker', label="Beaker session")
def define_beaker_option(group, configuration):
    group.add_argument('--beaker-data-dir',
                       dest='beaker.session.data_dir',
                       help="Used with any back-end that stores its data in "
                            "physical files, such as the dbm or file-based "
                            "back-ends. This path should be an absolute path "
                            "to the directory that stores the files.")
    group.add_argument('--beaker-lock-dir',
                       dest='beaker.session.lock_dir',
                       help="Used with every back-end, to coordinate locking. "
                            "With caching, this lock file is used to ensure "
                            "that multiple processes/threads aren’t "
                            "attempting to re-create the same value at the "
                            "same time (The Dog-Pile Effect)")
    group.add_argument('--beaker-memcache-module',
                       dest='beaker.session.memcache_module',
                       help="One of the names memcache, cmemcache, pylibmc, "
                            "or auto. Default is auto. Specifies which "
                            "memcached client library should be imported when "
                            "using the ext:memcached backend. If left at its "
                            "default of auto, pylibmc is favored first, then "
                            "cmemcache, then memcache.")
    group.add_argument('--beaker-type',
                       dest='beaker.session.type',
                       help="The name of the back-end to use for storing the "
                            "sessions or cache objects.\nAvailable back-ends "
                            "supplied with Beaker: file, dbm, memory, "
                            "ext:memcached, ext:database, ext:google\nFor "
                            "sessions, the additional type of cookie is "
                            "available which will store all the session data "
                            "in the cookie itself. As such, size limitations "
                            "apply (4096 bytes).\nSome of these back-ends "
                            "require the url option as listed below.")
    group.add_argument('--beaker-url',
                       dest='beaker.session.url',
                       help="URL is specific to use of either ext:memcached "
                            "or ext:database. When using one of those types, "
                            "this option is required. When used with "
                            "ext:memcached, this should be either a single, "
                            "or semi-colon separated list of memcached "
                            "servers When used with ext:database, this should "
                            "be a valid SQLAlchemy database string.")
    group.add_argument('--beaker-cookie-expires',
                       dest='beaker.session.cookie_expires',
                       help="Determines when the cookie used to track the "
                            "client-side of the session will expire. When set "
                            "to a boolean value, it will either expire at the "
                            "end of the browsers session, or never expire. "
                            "Setting to a datetime forces a hard ending time "
                            "for the session (generally used for setting a "
                            "session to a far off date). Setting to an "
                            "integer will result in the cookie being set to "
                            "expire in that many seconds. I.e. a value of 300 "
                            "will result in the cookie being set to expire in "
                            "300 seconds. Defaults to never expiring.")
    group.add_argument('--beaker-cookie-domain',
                       dest='beaker.session.cookie_domain',
                       help="What domain the cookie should be set to. When "
                            "using sub-domains, this should be set to the "
                            "main domain the cookie should be valid for. For "
                            "example, if a cookie should be valid under "
                            "www.nowhere.com and files.nowhere.com then it "
                            "should be set to .nowhere.com. Defaults to the "
                            "current domain in its entirety.")
    group.add_argument('--beaker-key',
                       dest='beaker.session.key',
                       help="Name of the cookie key used to save the session "
                            "under.")
    group.add_argument('--beaker-secret',
                       dest='beaker.session.secret',
                       help="Used with the HMAC to ensure session integrity. "
                            "This value should ideally be a randomly "
                            "generated string. When using in a cluster "
                            "environment, the secret must be the same on "
                            "every machine.")
    group.add_argument('--beaker-secure',
                       dest='beaker.session.secure',
                       help="Whether or not the session cookie should be "
                            "marked as secure. When marked as secure, "
                            "browsers are instructed to not send the cookie "
                            "over anything other than an SSL connection.")
    group.add_argument('--beaker-timeout',
                       dest='beaker.session.timeout',
                       help="Seconds until the session is considered invalid, "
                            "after which it will be ignored and invalidated. "
                            "This number is based on the time since the "
                            "session was last accessed, not from when the "
                            "session was created. Defaults to never expiring.")
    group.add_argument('--beaker-encrypt-key',
                       dest='beaker.session.encrypt_key',
                       help="Encryption key to use for the AES cipher. This "
                            "should be a fairly long randomly generated "
                            "string.")
    group.add_argument('--beaker-validate-key',
                       dest='beaker.session.validate_key',
                       help="Validation key used to sign the AES encrypted "
                            "data.")
