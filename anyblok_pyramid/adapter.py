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


def timedelta_adapter(obj, request, mode='seconds'):

    """Format the fields.TimeDelta to return String

    ::
        from pyramid.renderers import JSON
        from datetime import timedelta
        json_renderer = JSON()
        json_renderer.add_adapter(timedelta, timedelta_adapter)
        config.add_renderer('json', json_renderer)

    The mode parameter can be used to set the output of the adpater.
    This parameter can either be :

        * microseconds
        * milliseconds
        * seconds (default)
        * minutes
        * hours
        * days
        * weeks

    When using this adapter with non default parameter, it might be used the
    following way :

    ::
        from pyramid.renderers import JSON
        from datetime import timedelta
        json_renderer = JSON()
        json_renderer.add_adapter(
            timedelta, lambda obj, request: timedelta_adapter(
                obj, request, 'hours'))
        config.add_renderer('json', json_renderer)

    :param obj: timedelta obj
    :param mode: str
    :rtype: str, seconds corresponding to timedelta
    """

    seconds = obj.total_seconds()

    if mode == 'microseconds':
        # 1 second = 10**6 microseconds
        return seconds * 10**6
    elif mode == 'milliseconds':
        # 1 second = 10**3 milliseconds
        return seconds * 10**3
    elif mode == 'seconds':
        return seconds
    elif mode == 'minutes':
        # 1 minute = 60 seconds
        return seconds / 60
    elif mode == 'hours':
        # 1 hour = 60 minutes
        # 3600 = 60 * 60
        return seconds / 3600
    elif mode == 'days':
        # 1 day = 24 hours
        # 86400 = 60 * 60 * 24
        return seconds / 86400
    elif mode == 'weeks':
        # 1 week = 7 days
        # 604800 = 60 * 60 * 24 * 7
        return seconds / 604800
    else:
        raise ValueError(
            ("Provided mode for timedelta_adapter is not valid. Found '%s'"
             "." % mode
             )
            )

    return obj.total_seconds()


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
