# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.config import (define_preload_option,
                                    define_wsgi_option,
                                    define_wsgi_debug_option,
                                    add_configuration_file,
                                    update_plugins)
from anyblok.tests.testcase import TestCase
from anyblok.tests.test_config import MockArgumentParser


class TestArgsParseOption(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestArgsParseOption, cls).setUpClass()
        cls.parser = MockArgumentParser()
        cls.group = cls.parser.add_argument_group('label')
        cls.configuration = {}
        cls.function = {
            'define_preload_option': define_preload_option,
            'define_wsgi_option': define_wsgi_option,
            'define_wsgi_debug_option': define_wsgi_debug_option,
            'add_configuration_file': add_configuration_file,
            'update_plugins': update_plugins,
        }

    def test_define_preload_option(self):
        self.function['define_preload_option'](self.parser)

    def test_define_wsgi_option(self):
        self.function['define_wsgi_option'](self.parser)

    def test_define_wsgi_debug_option(self):
        self.function['define_wsgi_debug_option'](self.parser)

    def test_add_configuration_file(self):
        self.function['add_configuration_file'](self.parser)

    def test_update_plugins(self):
        self.function['update_plugins'](self.parser)
