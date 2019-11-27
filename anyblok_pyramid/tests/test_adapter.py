# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Alexis TOURNEUX <tourneuxalexis@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime, date, timedelta
from pyramid.renderers import JSON
from uuid import UUID, uuid1
from os import urandom
from decimal import Decimal
from anyblok_pyramid.adapter import (
    datetime_adapter,
    date_adapter,
    TimeDeltaModes,
    timedelta_adapter_factory,
    uuid_adapter,
    bytes_adapter,
    decimal_adapter,
)
from anyblok_pyramid.testing import init_web_server
import pytest


class TestAdapter:

    def test_registry_get_datetime(self):

        def get_datetime(request):
            return {'datetime': datetime(2017, 10, 1, 1, 1, 1)}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_datetime, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(datetime, datetime_adapter)
            config.add_renderer('json', json_renderer)

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert res.json_body['datetime'] == datetime_adapter(
            datetime(2017, 10, 1, 1, 1, 1), None)

    def test_registry_get_timedelta(self):

        def get_timedelta(request):
            return {'timedelta': timedelta(
                days=1, hours=4, minutes=56,
                seconds=3710, milliseconds=4000,
                microseconds=500)}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(
                get_timedelta, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(
                timedelta, timedelta_adapter_factory())
            config.add_renderer('json', json_renderer)

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)

        assert res.json_body['timedelta'] == timedelta(
            days=1, hours=4, minutes=56, seconds=3710,
            milliseconds=4000, microseconds=500).total_seconds()

        # This part is aimed at testing that the different modes implemented on
        # timedelta adapter are behaving as intented
        delta = timedelta(
            weeks=1, days=3, hours=15, minutes=3, seconds=45, milliseconds=354,
            microseconds=768
        )

        assert round(
            timedelta_adapter_factory(TimeDeltaModes.SECONDS)(
                delta, None), 8) == 918225.354768
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.MICROSECONDS)(
                delta, None), 8) == 918225354768
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.MILLISECONDS)(
                delta, None), 8) == 918225354.768
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.MINUTES)(
                delta, None), 8) == 15303.7559128
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.HOURS)(
                delta, None), 8) == 255.06259855
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.DAYS)(
                delta, None), 8) == 10.62760827
        assert round(
            timedelta_adapter_factory(TimeDeltaModes.WEEKS)(
                delta, None), 8) == 1.51822975

        with pytest.raises(ValueError):
            timedelta_adapter_factory("not a valid mode")(delta, None)

    def test_registry_get_date(self):

        def get_date(request):
            return {'date': date(2017, 10, 1)}

        def add_route_and_views(config):
            config.add_route('dbname', '/test/')
            config.add_view(get_date, route_name='dbname', renderer='json')
            json_renderer = JSON()
            json_renderer.add_adapter(date, date_adapter)
            config.add_renderer('json', json_renderer)

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert res.json_body['date'] == date_adapter(date(2017, 10, 1), None)

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

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert res.json_body['uuid'] == uuid_adapter(uuid, None)

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

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert res.json_body['bytes'] == bytes_adapter(val, None)

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

        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert res.json_body['decimal'] == decimal_adapter(val, None)
