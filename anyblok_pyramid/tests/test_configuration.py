# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.config import (
    define_wsgi_option,
    define_auth_option,
    define_wsgi_debug_option,
    add_configuration_file,
    update_plugins
)
from anyblok.tests.test_config import MockArgumentParser


class TestArgsParseOption:

    def test_define_wsgi_option(self):
        parser = MockArgumentParser()
        define_wsgi_option(parser)

    def test_define_auth_option(self):
        parser = MockArgumentParser()
        define_auth_option(parser)

    def test_define_wsgi_debug_option(self):
        parser = MockArgumentParser()
        define_wsgi_debug_option(parser)

    def test_add_configuration_file(self):
        parser = MockArgumentParser()
        add_configuration_file(parser)

    def test_update_plugins(self):
        parser = MockArgumentParser()
        update_plugins(parser)
