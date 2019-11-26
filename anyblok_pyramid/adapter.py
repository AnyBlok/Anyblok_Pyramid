# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2017 Franck BRET <franckbret@gmail.com>
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Alexis TOURNEUX <tourneuxalexis@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytz
import time
from base64 import b64encode
from decimal import Decimal
from datetime import timedelta


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

    if mode == 'microseconds':
        return obj / timedelta(microseconds=1)
    elif mode == 'milliseconds':
        return obj / timedelta(milliseconds=1)
    elif mode == 'seconds':
        return obj.total_seconds()
    elif mode == 'minutes':
        return obj / timedelta(minutes=1)
    elif mode == 'hours':
        return obj / timedelta(hours=1)
    elif mode == 'days':
        return obj / timedelta(days=1)
    elif mode == 'weeks':
        return obj / timedelta(weeks=1)
    else:
        raise ValueError(
            ("Provided mode for timedelta_adapter is not valid. Found '%s'"
             "." % mode))

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
