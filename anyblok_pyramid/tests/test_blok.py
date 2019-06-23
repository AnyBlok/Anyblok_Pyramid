# This file is a part of the AnyBlok project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest


class TestPyramidBlok:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_testblok):
        transaction = registry_testblok.begin_nested()
        request.addfinalizer(transaction.rollback)
        return

    def test_current_blok(self, registry_testblok, webserver):
        registry = registry_testblok
        webserver.get('/hello/JS/', status=404)
        registry.upgrade(install=('test-pyramid1',))
        resp = webserver.get('/hello/JS/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'Hello JS !!!')

    def test_simple_crud_security(self, registry_testblok, webserver):
        registry = registry_testblok
        registry.upgrade(install=('test-pyramid2',))
        webserver.get('/bloks', status=403)
        webserver.get('/blok/auth', status=403)
        resp = webserver.post_json(
            '/login', {'login': 'viewer', 'password': ''},
            status=302)
        headers = resp.headers
        webserver.get('/bloks', status=200, headers=headers)
        webserver.get('/blok/auth', status=200, headers=headers)
        webserver.put('/blok/auth', {}, status=403, headers=headers)
        resp = webserver.post('/logout', {}, status=302)
        headers = resp.headers
        webserver.get('/bloks', status=403, headers=headers)
        webserver.get('/blok/auth', status=403, headers=headers)
        resp = webserver.post_json(
            '/login', {'login': 'admin', 'password': ''},
            status=302)
        headers = resp.headers
        webserver.get('/bloks', status=200, headers=headers)
        webserver.get('/blok/auth', status=200, headers=headers)
        webserver.put('/blok/auth', {}, status=200, headers=headers)
