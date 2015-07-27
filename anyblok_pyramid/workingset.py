# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
# flake8: noqa
from pkg_resources import VersionConflict


class WorkingSetException(Exception):
    """Exception for Working set"""


class WorkingSet:
    """Allow to set and get callback::

        ws = WorkingSet._build_master()

        def mycallback():
            return True

        ws.set_callable(name='callback name', callback=mycallback)
        assert ws.get_callable('callback name')() is True

    An instance of the WorkingSet is already load by anyblok_pyramid and
    the method `set_callable`and `get_callable` is directly accessible::

        from anyblok_pyramid import set_callable, get_callable

        def mycallback():
            return True

        set_callable(name='callback name', callback=mycallback)
        assert get_callable('callback name')() is True
    """

    def __init__(self):
        self.callbacks = {}

    @classmethod
    def _build_master(cls):
        ws = cls()
        try:
            from __main__ import __requires__
        except ImportError:
            # The main program does not list any requirements
            return ws

        # ensure the requirements are met
        try:
            ws.require(__requires__)
        except VersionConflict:
            return cls._build_from_requirements(__requires__)

        return ws

    def get_callable(self, name, raiseifnotexist=True, default_callback=None):
        """Return the callable for the wanted callback
        ::

            from anyblok_pyramid import get_callable

            my_callback = get_callable('my callback')
            my_callback(...)

        :param name: name of the callback
        :param raiseifnotexist: boolean, raise if True and no callback found
        :param default_callback: return this callback if no callback found and
                                 raiseifnotexist is False
        :rtype: return the callback found
        :exception: WorkingSetException
        """
        if name in self.callbacks:
            return self.callbacks[name]
        elif raiseifnotexist:
            raise WorkingSetException("No callback found for %r" % name)
        elif default_callback:
            return default_callback
        else:

            def _callback(*args, **kwargs):
                return None

            return _callback

    def set_callable(self, name=None, callback=None):
        """Save a new callback

        You can set the callback by pointer::

            from anyblok_pyramid import set_callable

            def my_callback():
                return True

            set_callable(name='my_callback', callback=my_callback)

        You can set also by decorate the callable::

            from anyblok_pyramid import set_callable

            @set_callable()
            def my_callback():
                return True

        .. note::

            if you use the decoration mode, the name by default if the
            ``__name__`` of the callable
        """

        def wrapper(_callback, name=name):
            if name is None:
                name = _callback.__name__

            self.callbacks[name] = _callback
            return _callback

        if callback:
            return wrapper(callback)
        else:
            return wrapper
