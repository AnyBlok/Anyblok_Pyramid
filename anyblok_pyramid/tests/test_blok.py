# This file is a part of the AnyBlok project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidDBTestCase


class TestPyramidBlok(PyramidDBTestCase):

    blok_entry_points = ('bloks', 'test_bloks')

    def test_current_blok(self):
        registry = self.init_registry(None)
        self.webserver.get('/hello/JS/', status=404)
        registry.upgrade(install=('test-pyramid1',))
        resp = self.webserver.get('/hello/JS/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'Hello JS !!!')

    def test_simple_crud_security(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test-pyramid2',))
        self.webserver.get('/bloks', status=403)
        self.webserver.get('/blok/auth', status=403)
        resp = self.webserver.post_json(
            '/login', {'login': 'viewer', 'password': ''},
            status=302)
        headers = resp.headers
        self.webserver.get('/bloks', status=200, headers=headers)
        self.webserver.get('/blok/auth', status=200, headers=headers)
        self.webserver.put('/blok/auth', {}, status=403, headers=headers)
        resp = self.webserver.post('/logout', {}, status=302)
        headers = resp.headers
        self.webserver.get('/bloks', status=403, headers=headers)
        self.webserver.get('/blok/auth', status=403, headers=headers)
        resp = self.webserver.post_json(
            '/login', {'login': 'admin', 'password': ''},
            status=302)
        headers = resp.headers
        self.webserver.get('/bloks', status=200, headers=headers)
        self.webserver.get('/blok/auth', status=200, headers=headers)
        self.webserver.put('/blok/auth', {}, status=200, headers=headers)
