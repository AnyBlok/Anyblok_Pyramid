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
        registry.upgrade(install=('test-pyramid-blok1',))
        resp = self.webserver.get('/hello/JS/', status=200)
        self.assertEqual(resp.body.decode('utf8'), 'Hello JS !!!')
