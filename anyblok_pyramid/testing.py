# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import warnings
from anyblok.tests.testcase import DBTestCase, BlokTestCase
from webtest import TestApp
from .pyramid_config import Configurator


def init_web_server(*functions):
    config = Configurator()
    config.include_from_entry_point()
    for function in functions:
        config.include(function)

    config.load_config_bloks()
    app = config.make_wsgi_app()
    return TestApp(app)


class PyramidTestCase:

    @classmethod
    def setUpClass(cls):
        warnings.warn(
            "The testCase from anyblok_pyramid for nose are deprecated. "
            "Refactor all your unittest with pytest: %r" % cls,
            DeprecationWarning, stacklevel=2)
        super(PyramidTestCase, cls).setUpClass()

    def setUp(self):
        super(PyramidTestCase, self).setUp()
        self.includemes = []

    def init_web_server(self):
        return init_web_server(*self.includemes)


class PyramidDBTestCase(PyramidTestCase, DBTestCase):

    def init_registry_with_bloks(self, *args, **kwargs):
        res = super(PyramidDBTestCase, self).init_registry_with_bloks(
            *args, **kwargs)
        self.webserver = self.init_web_server()
        return res


class PyramidBlokTestCase(PyramidTestCase, BlokTestCase):

    @property
    def webserver(self):
        return self.init_web_server()
