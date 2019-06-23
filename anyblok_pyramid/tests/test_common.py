# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok.testing import LogCapture, tmp_configuration
from anyblok.config import Configuration
from anyblok_pyramid.common import get_registry_for, preload_databases
from sqlalchemy.exc import ResourceClosedError
from logging import INFO, WARNING


class TestCommon:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_testblok):
        transaction = registry_testblok.begin_nested()

        def rollback():
            try:
                transaction.rollback()
            except ResourceClosedError:
                pass

        request.addfinalizer(rollback)
        return

    def test_get_registry_for(self, registry_testblok):
        registry = get_registry_for(Configuration.get('db_name'))
        assert registry is not None

    def test_preload_databases(self):
        db_name = Configuration.get('db_name')
        with tmp_configuration(db_names=[db_name]):
            with LogCapture('anyblok_pyramid.common', level=INFO) as handler:
                preload_databases()
                messages = handler.get_info_messages()
                assert messages
                assert 'The database %r is preloaded' % db_name in messages

    def test_preload_unexisting_databases(self):
        db_name = 'wrong_db_name'
        with tmp_configuration(db_names=[db_name]):
            with LogCapture('anyblok_pyramid.common', level=WARNING) as handler:
                preload_databases()
                messages = handler.get_warning_messages()
                assert messages
                assert 'The database %r does not exist' % db_name in messages
