# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from copy import deepcopy
from anyblok_pyramid import merge
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


@pytest.mark.parametrize(
    "d1,d2,expected",
    [
        (
            {"a": {"b": {"c": "d"}}},
            {"a": {"b": {"e": "f"}}},
            {"a": {"b": {"c": "d", "e": "f"}}},
        ),
        (
            {"a": {"b": {"c": "d"}}},
            {},
            {"a": {"b": {"c": "d"}}},
        ),
        (
            {},
            {"a": {"b": {"c": "d"}}},
            {"a": {"b": {"c": "d"}}},
        ),
        (
            {"a": 1},
            {"a": 2},
            {"a": 2},
        ),
        (
            {"a": 1},
            {"a": {"b": "c"}},
            {"a": {"b": "c"}},
        ),
        (
            {"a": {"b": "c"}},
            {"a": 1},
            {"a": 1},
        ),
        (
            {"a": {"b": {"c": "d"}}},
            {"a": {"c": 1}},
            {"a": {"b": {"c": "d"}, "c": 1}},
        ),
        (
            {"a": {"c": 1}},
            {"a": {"b": {"c": "d"}}},
            {"a": {"b": {"c": "d"}, "c": 1}},
        ),
        (
            {"a": {"b": {"c": "d", "e": "z", "g": "h"}}},
            {"a": {"b": {"e": "f"}}},
            {"a": {"b": {"c": "d", "e": "f", "g": "h"}}},
        ),
        (
            {"a": {"b": ["c", "d"]}},
            {"a": {"b": ["e", "f"]}},
            {"a": {"b": ["c", "d", "e", "f"]}},
        ),
        (
            {"a": {"b": ["c"]}},
            {"a": 1},
            {"a": 1},
        ),
        (
            {"a": 1},
            {"a": {"b": ["c"]}},
            {"a": {"b": ["c"]}},
        ),
        (
            {"a": {"b": {"c": "d"}}},
            {"a": {"b": ["c"]}},
            {"a": {"b": ["c"]}},
        ),
        (
            {"a": {"b": ["c"]}},
            {"a": {"b": {"c": "d"}}},
            {"a": {"b": {"c": "d"}}},
        ),
        (
            {"a": {"b": ["c"]}},
            {"a": {"c": 1}},
            {"a": {"b": ["c"], "c": 1}},
        ),
        (
            {"a": {"c": 1}},
            {"a": {"b": ["c"]}},
            {"a": {"b": ["c"], "c": 1}},
        ),
    ],
)
def test_merge(d1, d2, expected):
    copy_d1 = deepcopy(d1)
    copy_d2 = deepcopy(d2)
    assert merge(d1, d2) == expected
    assert d1 == copy_d1
    assert d2 == copy_d2
