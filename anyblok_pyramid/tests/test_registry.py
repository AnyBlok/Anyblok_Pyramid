# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from pyramid.response import Response
from anyblok.config import Configuration
from anyblok_pyramid.config import get_db_name
from anyblok_pyramid.testing import init_web_server


def _get_db_name(request):
    dbname = None
    if request.anyblok.registry:
        dbname = request.anyblok.registry.db_name

    return Response(dbname)


class TestRegistry:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_blok):
        transaction = registry_blok.begin_nested()

        def rollback():
            transaction.rollback()
            Configuration.update(get_db_name=get_db_name)

        request.addfinalizer(rollback)
        return

    def add_route_and_views(self, config):
        config.add_route('dbname', '/test/')
        config.add_view(_get_db_name, route_name='dbname')

    def test_registry_by_default_method(self, registry_blok):
        webserver = init_web_server(self.add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert Configuration.get('db_name') == res.body.decode('utf8')

    def test_registry_by_wrong_name(self, registry_blok):
        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(self.add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert not res.body

    def test_registry_by_path(self, registry_blok):
        def __get_db_name(request):
            return request.matchdict['dbname']

        def add_route_and_views(config):
            config.add_route('dbname', '/test/{dbname}/')
            config.add_view(_get_db_name, route_name='dbname')

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/%s/' % Configuration.get('db_name'),
                            status=200)

        assert Configuration.get('db_name') == res.body.decode('utf8')
        res = webserver.get('/test/wrong_db_name/', status=200)
        assert not res.body
