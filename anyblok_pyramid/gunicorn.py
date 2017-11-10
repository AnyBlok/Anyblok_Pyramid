# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from gunicorn.config import (Config as GunicornConfig,
                             Setting, validate_callable, validate_post_request)
from gunicorn.app.base import Application
from gunicorn import __version__
from anyblok.config import Configuration, getParser
from anyblok.blok import BlokManager
from .pyramid_config import Configurator
import argparse
import six
from anyblok import (
    load_init_function_from_entry_points,
    configuration_post_load,
)
from .common import preload_databases
from logging import getLogger
logger = getLogger(__name__)


class Config(GunicornConfig):

    def __init__(self, usage=None, prog=None, application=None,
                 configuration_groups=None):
        super(Config, self).__init__(usage=usage, prog=prog)
        self.configuration_groups = configuration_groups
        self.application = application

    def parser(self):
        # Don't call super to user the Parser of anyblok
        kwargs = {
            "usage": self.usage,
            "prog": self.prog
        }
        parser = getParser(**kwargs)
        parser.add_argument("-v", "--version",
                            action="version", default=argparse.SUPPRESS,
                            version="%(prog)s (version " + __version__ + ")\n",
                            help="show program's version number and exit")
        parser.add_argument("args", nargs="*", help=argparse.SUPPRESS)

        keys = sorted(self.settings, key=self.settings.__getitem__)
        for k in keys:
            self.settings[k].add_option(parser)

        description = {}
        if self.application in Configuration.applications:
            description.update(Configuration.applications[self.application])
        else:
            description.update(Configuration.applications['default'])

        _configuration_groups = description.pop('configuration_groups',
                                                ['gunicorn', 'database'])
        if 'plugins' not in _configuration_groups:
            _configuration_groups.append('plugins')

        configuration_groups = set(self.configuration_groups or []).union(
            _configuration_groups)
        Configuration._load(parser, configuration_groups,
                            ('AnyBlok', 'bloks'))
        return parser

    def set(self, name, value):
        if name not in self.settings:
            return  # certainly come from anyblok config

        self.settings[name].set(value)


class WSGIApplication(Application):

    def __init__(self, application, configuration_groups=None):
        self.configuration_groups = configuration_groups
        load_init_function_from_entry_points()
        conf = Configuration.applications.get(application, {})
        usage = conf.get('usage')
        prog = conf.get('prog')
        self.application = application
        super(WSGIApplication, self).__init__(usage=usage, prog=prog)

    def load_default_config(self):
        self.cfg = Config(self.usage, prog=self.prog,
                          application=self.application,
                          configuration_groups=self.configuration_groups)

    def init(self, parser, opts, args):
        Configuration.parse_options(opts, ('gunicorn',))

        # get the configuration save in AnyBlok configuration in
        # gunicorn configuration
        for name in Configuration.configuration.keys():
            if name in self.cfg.settings:
                value = Configuration.get(name)
                if value:
                    self.cfg.settings[name].set(value)

        configuration_post_load()

    def load(self):
        BlokManager.load()
        preload_databases()
        config = Configurator()
        config.include_from_entry_point()
        config.load_config_bloks()
        return config.make_wsgi_app()


class PreRequest(Setting):
    name = "pre_request"
    section = "Server Hooks"
    validator = validate_callable(2)
    type = six.callable

    def pre_request(worker, req):
        logger.info("PRE-REQUEST => %s %s" % (req.method, req.path))

    default = staticmethod(pre_request)
    desc = """\
        Called just before a worker processes the request.

        The callable needs to accept two instance variables for the Worker and
        the Request.
    """


class PostRequest(Setting):
    name = "post_request"
    section = "Server Hooks"
    validator = validate_post_request
    type = six.callable

    def post_request(worker, req, environ, resp):
        logger.info("POST-REQUEST => %s %s | %r" % (
            req.method, req.path, resp.status))

    default = staticmethod(post_request)
    desc = """\
        Called after a worker processes the request.

        The callable needs to accept two instance variables for the Worker and
        the Request.
    """
