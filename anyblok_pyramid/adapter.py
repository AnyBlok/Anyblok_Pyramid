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

from enum import Enum, unique


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


@unique
class TimeDeltaModes(Enum):

    """This enum is aimed at creating constants for setting the serialization
       mode for timedelta adapter."""

    MICROSECONDS = 1
    MILLISECONDS = 2
    SECONDS = 3
    MINUTES = 4
    HOURS = 5
    DAYS = 6
    WEEKS = 7


def timedelta_adapter_factory(mode=TimeDeltaModes.SECONDS):
    def timedelta_adapter(obj, request):

        """Format the fields.TimeDelta to return String

        ::
            from pyramid.renderers import JSON
            from datetime import timedelta
            from anyblok_pyramid.adapter import timedelta_adapter_factory
            json_renderer = JSON()
            json_renderer.add_adapter(timedelta, timedelta_adapter_factory())
            config.add_renderer('json', json_renderer)

        The mode parameter can be used to set the output of the adapter.
        This parameter can either be :

            * microseconds -> TimeDeltaModes.MICROSECONDS
            * milliseconds -> TimeDeltaModes.MILLISECONDS
            * seconds (default) -> TimeDeltaModes.SECONDS
            * minutes -> TimeDeltaModes.MINUTES
            * hours -> TimeDeltaModes.HOURS
            * days -> TimeDeltaModes.DAYS
            * weeks -> TimeDeltaModes.WEEKS

        When using this adapter with non default parameter, it might be used the
        following way :

        ::
            from pyramid.renderers import JSON
            from datetime import timedelta
            from anyblok_pyramid.adapter import (
                timedelta_adapter_factory,
                TimeDeltaModes
            )

            json_renderer = JSON()
            json_renderer.add_adapter(
                timedelta, timedelta_adapter_factory(TimeDeltaModes.HOURS))
            config.add_renderer('json', json_renderer)

        :param obj: timedelta obj
        :param mode: str
        :rtype: str, seconds corresponding to timedelta
        """

        if mode == TimeDeltaModes.MICROSECONDS:
            return obj / timedelta(microseconds=1)
        elif mode == TimeDeltaModes.MILLISECONDS:
            return obj / timedelta(milliseconds=1)
        elif mode == TimeDeltaModes.SECONDS:
            return obj.total_seconds()
        elif mode == TimeDeltaModes.MINUTES:
            return obj / timedelta(minutes=1)
        elif mode == TimeDeltaModes.HOURS:
            return obj / timedelta(hours=1)
        elif mode == TimeDeltaModes.DAYS:
            return obj / timedelta(days=1)
        elif mode == TimeDeltaModes.WEEKS:
            return obj / timedelta(weeks=1)
        else:
            raise ValueError(
                ("Provided mode for timedelta_adapter is not valid. Found '%s'"
                 "." % mode))

    return timedelta_adapter


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


def enum_adapter(obj, request):
    """Format the fields.Enum to return String

    ::

        from pyramid.renderers import JSON
        import enum

        json_renderer = JSON()
        json_renderer.add_adapter(enum.Enum, enum_adapter)
        config.add_renderer('json', json_renderer)


    :param obj: Enum
    :rtype: str
    """
    return obj.value
