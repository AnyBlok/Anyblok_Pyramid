# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import DBTestCase, LogCapture
from anyblok.config import Configuration
from anyblok_pyramid.common import get_registry_for, preload_databases
from logging import INFO, WARNING


class TestCommon(DBTestCase):

    def test_get_registry_for(self):
        registry = get_registry_for(Configuration.get('db_name'))
        self.assertIsNotNone(registry)

    def test_preload_databases(self):
        db_name = Configuration.get('db_name')
        with DBTestCase.Configuration(db_names=[db_name]):
            with LogCapture('anyblok_pyramid.common', level=INFO) as handler:
                preload_databases()
                messages = handler.get_info_messages()
                self.assertTrue(messages)
                self.assertIn('The database %r is preloaded' % db_name,
                              messages)

    def test_preload_unexisting_databases(self):
        db_name = 'wrong_db_name'
        with DBTestCase.Configuration(db_names=[db_name]):
            with LogCapture('anyblok_pyramid.common', level=WARNING) as handler:
                preload_databases()
                messages = handler.get_warning_messages()
                self.assertTrue(messages)
                self.assertIn('The database %r does not exist' % db_name,
                              messages)
