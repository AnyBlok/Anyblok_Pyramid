# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .testcase import PyramidDBTestCase
from datetime import datetime, date
from pyramid.renderers import JSON
from uuid import UUID, uuid1
from os import urandom
from decimal import Decimal
from anyblok_pyramid.adapter import (
    datetime_adapter,
    date_adapter,
    uuid_adapter,
    bytes_adapter,
    decimal_adapter,
)


class TestAdapter(PyramidDBTestCase):

    def test_registry_get_datetime(self):

        def get_datetime(request):
            return {'datetime': datetime(2017, 10, 1, 1, 1, 1)}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_datetime, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(datetime, datetime_adapter)
            config.add_renderer('json', json_renderer)

        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(
            res.json_body['datetime'],
            datetime_adapter(datetime(2017, 10, 1, 1, 1, 1), None)
        )

    def test_registry_get_date(self):

        def get_date(request):
            return {'date': date(2017, 10, 1)}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_date, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(date, date_adapter)
            config.add_renderer('json', json_renderer)

        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(
            res.json_body['date'],
            date_adapter(date(2017, 10, 1), None)
        )

    def test_registry_get_uuid(self):

        uuid = uuid1()

        def get_uuid(request):
            return {'uuid': uuid}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_uuid, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(UUID, uuid_adapter)
            config.add_renderer('json', json_renderer)

        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(
            res.json_body['uuid'],
            uuid_adapter(uuid, None)
        )

    def test_registry_get_bytes(self):

        val = urandom(100)

        def get_bytes(request):
            return {'bytes': val}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_bytes, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(bytes, bytes_adapter)
            config.add_renderer('json', json_renderer)

        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(
            res.json_body['bytes'],
            bytes_adapter(val, None)
        )

    def test_registry_get_decimal(self):

        val = Decimal('100.12')

        def get_bytes(request):
            return {'decimal': val}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_bytes, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(Decimal, decimal_adapter)
            config.add_renderer('json', json_renderer)

        self.includemes.append(add_route_and_views)
        webserver = self.init_web_server()
        res = webserver.get('/test/', status=200)
        self.assertEqual(
            res.json_body['decimal'],
            decimal_adapter(val, None)
        )
