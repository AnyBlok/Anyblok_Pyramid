# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.configuration import (define_wsgi_option,
                                           define_beaker_option,
                                           define_wsgi_debug_option)
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
            'define_wsgi_option': define_wsgi_option,
            'define_beaker_option': define_beaker_option,
            'define_wsgi_debug_option': define_wsgi_debug_option,
        }

    def test_define_wsgi_option(self):
        self.function['define_wsgi_option'](self.parser, self.configuration)

    def test_define_beaker_option(self):
        self.function['define_beaker_option'](self.parser, self.configuration)

    def test_define_wsgi_debug_option(self):
        self.function['define_wsgi_debug_option'](self.parser,
                                                  self.configuration)
