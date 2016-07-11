# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .testcase import PyramidDBTestCase
from pyramid.response import Response
from anyblok_pyramid.config import get_db_name
from anyblok.config import Configuration


def uninstalled(request):
    return Response('ko')


def installed(request):
    return Response('ok')


class TestViewPredicate(PyramidDBTestCase):

    def setUp(self):
        super(TestViewPredicate, self).setUp()
        self.installed_blok = 'anyblok-core'
        self.need_anyblok_registry = True

    def tearDown(self):
        super(TestViewPredicate, self).tearDown()
        Configuration.update(get_db_name=get_db_name)

    def add_route_and_views(self, config):
        config.add_route('test', '/test/')
        config.add_view(uninstalled, route_name='test')
        config.add_view(installed, route_name='test',
                        installed_blok=self.installed_blok)

    def add_route_and_views2(self, config):
        config.add_route('test', '/test/')
        config.add_view(installed, route_name='test',
                        need_anyblok_registry=self.need_anyblok_registry)

    def assetOK(self):
        resp = self.webserver.get('/test/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'ok')

    def assetKO(self):
        resp = self.webserver.get('/test/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'ko')

    def test_installed_blok(self):
        self.includemes.append(self.add_route_and_views)
        self.init_registry(None)
        self.assetOK()

    def test_uninstalled_blok(self):
        self.installed_blok = 'anyblok-io'
        self.includemes.append(self.add_route_and_views)
        self.init_registry(None)
        self.assetKO()

    def test_before_and_after_install_blok(self):
        self.installed_blok = 'anyblok-io'
        self.includemes.append(self.add_route_and_views)
        registry = self.init_registry(None)
        self.assetKO()
        registry.upgrade(install=['anyblok-io'])
        self.assetOK()
        registry.upgrade(uninstall=['anyblok-io'])
        self.assetKO()

    def test_need_anyblok_registry_ok(self):
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=200)

    def test_need_anyblok_registry_ko(self):
        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok2(self):
        self.need_anyblok_registry = False

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=200)


class TestRoutePredicate(PyramidDBTestCase):

    def setUp(self):
        super(TestRoutePredicate, self).setUp()
        self.installed_blok = 'anyblok-core'
        self.need_anyblok_registry = True

    def tearDown(self):
        super(TestRoutePredicate, self).tearDown()
        Configuration.update(get_db_name=get_db_name)

    def add_route_and_views(self, config):
        config.add_route('test', '/test/', installed_blok=self.installed_blok)
        config.add_view(installed, route_name='test')

    def add_route_and_views2(self, config):
        config.add_route('test', '/test/')
        config.add_view(installed, route_name='test',
                        need_anyblok_registry=self.need_anyblok_registry)

    def assetOK(self):
        resp = self.webserver.get('/test/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'ok')

    def test_installed_blok(self):
        self.includemes.append(self.add_route_and_views)
        self.init_registry(None)
        self.assetOK()

    def test_uninstalled_blok(self):
        self.installed_blok = 'anyblok-io'
        self.includemes.append(self.add_route_and_views)
        self.init_registry(None)
        self.webserver.get('/test/', status=404)

    def test_before_and_after_install_blok(self):
        self.installed_blok = 'anyblok-io'
        self.includemes.append(self.add_route_and_views)
        registry = self.init_registry(None)
        self.webserver.get('/test/', status=404)
        registry.upgrade(install=['anyblok-io'])
        self.assetOK()
        registry.upgrade(uninstall=['anyblok-io'])
        self.webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok(self):
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=200)

    def test_need_anyblok_registry_ko(self):
        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=404)

    def test_need_anyblok_registry_ok2(self):
        self.need_anyblok_registry = False

        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(self.add_route_and_views2)
        webserver = self.init_web_server()
        webserver.get('/test/', status=200)
