# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2017 Franck BRET <franckbret@gmail.com>
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytz
import time
from base64 import b64encode
from decimal import Decimal


def datetime_adapter(obj, request):
    """Format the fields.DateTime to return String

    If the datetime hasn't any timezone, force the timezone by
    the server timezone

    ::

        from pyramid.renderers import JSON
        from datetime import datetime
        json_renderer = JSON()
        json_renderer.add_adapter(datetime, datetime_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: datetime obj
    :rtype: str, isoformat datetime
    """
    if obj is not None:
        if obj.tzinfo is None:
            timezone = pytz.timezone(time.tzname[0])
            obj = timezone.localize(obj)

    return obj.isoformat()


def date_adapter(obj, request):
    """Format the fields.Date to return String

    ::

        from pyramid.renderers import JSON
        from datetime import date
        json_renderer = JSON()
        json_renderer.add_adapter(date, date_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: datetime obj
    :rtype: str, isoformat datetime
    """
    return obj.isoformat()


def uuid_adapter(obj, request):
    """Format the fields.UUID to return String

    ::

        from pyramid.renderers import JSON
        from uuid import UUID
        json_renderer = JSON()
        json_renderer.add_adapter(UUID, uuid_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: uuid obj
    :rtype: str
    """
    return str(obj.hex)


def bytes_adapter(obj, request):
    """Format the fields.Binary to return String

    ::

        from pyramid.renderers import JSON
        json_renderer = JSON()
        json_renderer.add_adapter(bytes, bytes_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: bytes
    :rtype: str
    """
    return b64encode(obj).decode("utf-8")


def decimal_adapter(obj, request):
    """Format the fields.Decimal to return String

    ::

        from pyramid.renderers import JSON
        json_renderer = JSON()
        json_renderer.add_adapter(Decimal, decimal_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: Decimal
    :rtype: str
    """
    return str(Decimal(obj).quantize(Decimal('1.00')))
