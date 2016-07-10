# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .testcase import PyramidDBTestCase
from anyblok.config import Configuration
from pyramid.response import Response
from anyblok_pyramid.config import get_db_name


def _get_db_name(request):
    dbname = None
    if request.anyblok.registry:
        dbname = request.anyblok.registry.db_name

    return Response(dbname)


class TestRegistry(PyramidDBTestCase):

    def tearDown(self):
        super(TestRegistry, self).tearDown()
        Configuration.update(get_db_name=get_db_name)

    def add_route_and_views(self, config):
        config.add_route('dbname', '/test/')
        config.add_view(_get_db_name, route_name='dbname')

    def test_registry_by_default_method(self):
        self.includemes.append(self.add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(Configuration.get('db_name'), res.body.decode('utf8'))

    def test_registry_by_wrong_name(self):
        def __get_db_name(request):
            return 'wrong_db_name'

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(self.add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertFalse(res.body)

    def test_registry_by_path(self):
        def __get_db_name(request):
            return request.matchdict['dbname']

        def add_route_and_views(config):
            config.add_route('dbname', '/test/{dbname}/')
            config.add_view(_get_db_name, route_name='dbname')

        Configuration.update(get_db_name=__get_db_name)
        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/%s/' % Configuration.get('db_name'),
                            status=200)
        self.assertEqual(Configuration.get('db_name'), res.body.decode('utf8'))
        res = webserver.get('/test/wrong_db_name/', status=200)
        self.assertFalse(res.body)
