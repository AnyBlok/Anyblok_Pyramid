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


def uninstalled(request):
    return Response('ko')


def installed(request):
    return Response('ok')


class TestRoutePredicate:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_blok):
        transaction = registry_blok.begin_nested()

        def rollback():
            transaction.rollback()
            Configuration.update(get_db_name=get_db_name)

        request.addfinalizer(rollback)
        return

    def add_route_and_views(self, config):
        config.add_route('test', '/test/', installed_blok=self.installed_blok)
        config.add_view(installed, route_name='test')

    def add_route_and_views2(self, config):
        config.add_route('test', '/test/',
                         need_anyblok_registry=self.need_anyblok_registry)
        config.add_view(installed, route_name='test')

    def assertOK(self, webserver):
        resp = webserver.get('/test/', status=200)
        assert resp.body.decode('utf8') == 'ok'

    def test_installed_blok(self, registry_blok):
        self.installed_blok = 'anyblok-core'
        webserver = init_web_server(self.add_route_and_views)
        self.assertOK(webserver)

    def test_uninstalled_blok(self, registry_blok):
        self.installed_blok = 'anyblok-io'
        webserver = init_web_server(self.add_route_and_views)
        webserver.get('/test/', status=404)

    def test_before_and_after_install_blok(self, registry_blok):
        self.installed_blok = 'auth'
        webserver = init_web_server(self.add_route_and_views)
        webserver.get('/test/', status=404)
        registry_blok.upgrade(install=['auth'])
        self.assertOK(webserver)
        registry_blok.upgrade(uninstall=['auth'])
        webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok(self, registry_blok):
        self.need_anyblok_registry = True
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=200)

    def test_need_anyblok_registry_ko(self, registry_blok):
        self.need_anyblok_registry = True

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok2(self, registry_blok):
        self.need_anyblok_registry = False

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=200)


class TestViewPredicate:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_blok):
        transaction = registry_blok.begin_nested()

        def rollback():
            transaction.rollback()
            Configuration.update(get_db_name=get_db_name)

        request.addfinalizer(rollback)
        return

    def add_route_and_views(self, config):
        config.add_route('test', '/test/')
        config.add_view(uninstalled, route_name='test')
        config.add_view(installed, route_name='test',
                        installed_blok=self.installed_blok)

    def add_route_and_views2(self, config):
        config.add_route('test', '/test/')
        config.add_view(installed, route_name='test',
                        need_anyblok_registry=self.need_anyblok_registry)

    def assertOK(self, webserver):
        resp = webserver.get('/test/', status=200)
        assert resp.body.decode('utf8') == 'ok'

    def assertKO(self, webserver):
        resp = webserver.get('/test/', status=200)
        assert resp.body.decode('utf8') == 'ko'

    def test_installed_blok(self, registry_blok):
        self.installed_blok = 'anyblok-core'
        webserver = init_web_server(self.add_route_and_views)
        self.assertOK(webserver)

    def test_uninstalled_blok(self, registry_blok):
        self.installed_blok = 'anyblok-io'
        webserver = init_web_server(self.add_route_and_views)
        self.assertKO(webserver)

    def test_before_and_after_install_blok(self, registry_blok):
        self.installed_blok = 'auth'
        webserver = init_web_server(self.add_route_and_views)
        self.assertKO(webserver)
        registry_blok.upgrade(install=['auth'])
        self.assertOK(webserver)
        registry_blok.upgrade(uninstall=['auth'])
        self.assertKO(webserver)

    def test_need_anyblok_registry_ok(self):
        self.need_anyblok_registry = True
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=200)

    def test_need_anyblok_registry_ko(self):
        self.need_anyblok_registry = True

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok2(self):
        self.need_anyblok_registry = False

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        webserver = init_web_server(self.add_route_and_views2)
        webserver.get('/test/', status=200)
