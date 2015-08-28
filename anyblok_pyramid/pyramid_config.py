# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from os.path import join
from pyramid.config import Configurator as PConfigurator
from anyblok.blok import BlokManager
from anyblok.config import Configuration
from .handler import HandlerHTTP, HandlerRPC
from pkg_resources import iter_entry_points
from .controllers import (Pyramid, PyramidHTTP, PyramidJsonRPC, PyramidXmlRPC,
                          PyramidException)
from logging import getLogger
logger = getLogger(__name__)


class Configurator(PConfigurator):
    """Overwrite the Pyramid Configurator"""

    def __init__(self, *args, **kwargs):
        kwargs = self.default_kwargs(**kwargs)
        super(Configurator, self).__init__(*args, **kwargs)

    def default_kwargs(self, **kwargs):
        if 'settings' not in kwargs:
            kwargs['settings'] = self.default_setting()

        return kwargs

    def default_setting(self):
        """Call all the entry point ``anyblok_pyramid.settings`` to update
        the argument setting

        the callable need to have one parametter, it is a dict::

            def settings_callable(setting):
                ...

        We add the entry point by the setup file::

            setup(
                ...,
                entry_points={
                    'anyblok_pyramid.settings': [
                        settings_callable=path:settings_callable,
                        ...
                    ],
                },
                ...,
            )


        """
        settings = {}
        for i in iter_entry_points('anyblok_pyramid.settings'):
            logger.debug('Load settings: %r' % i.name)
            i.load()(settings)

        return settings

    def include_from_entry_point(self):
        """Call all the entry point ``anyblok_pyramid.includeme`` to update
        the pyramid configuration

        the callable need to have one parametter(the instance of
        ``Configurator`` class, self)::

            def config_callable(config):
                config.include(...)

        We add the entry point by the setup file::

            setup(
                ...,
                entry_points={
                    'anyblok_pyramid.includeme': [
                        config_callable=path:config_callable,
                        ...
                    ],
                },
                ...,
            )


        """
        for i in iter_entry_points('anyblok_pyramid.includeme'):
            logger.debug('Load includeme: %r' % i.name)
            i.load()(self)


def pyramid_settings(settings):
    """Add in settings the default value for pyramid configuration

    :param settings: dict of the existing settings
    """
    settings.update({
        'pyramid.reload_templates': Configuration.get(
            'pyramid.reload_templates'),
        'pyramid.reload_assets': Configuration.get('pyramid.reload_assets'),
        'pyramid.debug_notfound': Configuration.get(
            'pyramid.debug_notfound'),
        'pyramid.debug_routematch': Configuration.get(
            'pyramid.debug_routematch'),
        'pyramid.prevent_http_cache': Configuration.get(
            'pyramid.prevent_http_cache'),
        'pyramid.debug_all': Configuration.get('pyramid.debug_all'),
        'pyramid.reload_all': Configuration.get('pyramid.reload_all'),
        'pyramid.default_locale_name': Configuration.get(
            'pyramid.default_locale_name'),
    })


def beaker_settings(settings):
    """Add in settings the default value for beaker configuration

    :param settings: dict of the existing settings
    """
    settings.update({
        'beaker.session.data_dir': Configuration.get(
            'beaker.session.data_dir'),
        'beaker.session.lock_dir': Configuration.get(
            'beaker.session.lock_dir'),
        'beaker.session.memcache_module': Configuration.get(
            'beaker.session.memcache_module'),
        'beaker.session.type': Configuration.get(
            'beaker.session.type'),
        'beaker.session.url': Configuration.get(
            'beaker.session.url'),
        'beaker.session.cookie_expires': Configuration.get(
            'beaker.session.cookie_expires'),
        'beaker.session.cookie_domain': Configuration.get(
            'beaker.session.cookie_domain'),
        'beaker.session.key': Configuration.get('beaker.session.key'),
        'beaker.session.secret': Configuration.get('beaker.session.secret'),
        'beaker.session.secure': Configuration.get('beaker.session.secure'),
        'beaker.session.timeout': Configuration.get(
            'beaker.session.timeout'),
        'beaker.session.encrypt_key': Configuration.get(
            'beaker.session.encrypt_key'),
        'beaker.session.validate_key': Configuration.get(
            'beaker.session.validate_key'),
    })


def pyramid_beaker(config):
    """Add beaker includeme in pyramid configuration

    :param config: Pyramid configurator instance
    """

    config.include('pyramid_beaker')


def declare_static(config):
    """Pyramid includeme, add the static path of the blok

    :param config: Pyramid configurator instance
    """

    for blok, cls in BlokManager.bloks.items():
        if hasattr(cls, 'static_paths'):
            paths = cls.static_paths
            if isinstance(paths, str):
                paths = [paths]
        else:
            paths = ['static']

        blok_path = BlokManager.getPath(blok)

        for p in paths:
            config.add_static_view(join(blok, p), join(blok_path, p))


def pyramid_config(config):
    """Pyramid includeme, add the route and view which are not
    added in the blok

    :param config: Pyramid configurator instance
    """
    for args, kwargs in Pyramid.routes:
        config.add_route(*args, **kwargs)

    for function, properties in Pyramid.views:
        config.add_view(function, **properties)


def pyramid_http_config(config):
    """ Pyramid includemee, add the route and view which are
    added in the blok by ``PyramidHTTP`` Type

    :param config: Pyramid configurator instance
    :exception: PyramidException
    """
    for args, kwargs in PyramidHTTP.routes:
        config.add_route(*args, **kwargs)

    endpoints = [x[0][0] for x in PyramidHTTP.routes]
    for hargs, properties in PyramidHTTP.views.items():
        if hargs[1] not in endpoints:
            raise PyramidException(
                "One or more %s controller has been declared but no route have"
                " declared" % hargs[1])
        config.add_view(HandlerHTTP(*hargs).wrap_view, **properties)


def _pyramid_rpc_config(cls, add_endpoint, add_method):
    """ Add the route and view which are added in the blok

    :param cls: PyramidRPC Type
    :param add_endpoint: function to add route in configuation
    :param add_method: function to add rpc_method in configuration
    :exception: PyramidException
    """
    for args, kwargs in cls.routes:
        add_endpoint(*args, **kwargs)

    endpoints = [x[0][0] for x in cls.routes]
    for namespace in cls.methods:
        if namespace not in endpoints:
            raise PyramidException(
                "One or more %s controller has been declared but no route have"
                " declared" % namespace)
        for method in cls.methods[namespace]:
            rpc_method = cls.methods[namespace][method]
            add_method(HandlerRPC(namespace, method).wrap_view,
                       route_name=namespace,
                       **rpc_method)


def pyramid_jsonrpc_config(config):
    """ Pyramid includemee, add the route and view which are
    added in the blok by ``PyramidJsonRPC`` Type

    :param config: Pyramid configurator instance
    """
    config.include('pyramid_rpc.jsonrpc')
    _pyramid_rpc_config(
        PyramidJsonRPC, config.add_jsonrpc_endpoint, config.add_jsonrpc_method)


def pyramid_xmlrpc_config(config):
    """ Pyramid includemee, add the route and view which are
    added in the blok by ``PyramidXmlRPC`` Type

    :param config: Pyramid configurator instance
    """
    config.include('pyramid_rpc.xmlrpc')
    _pyramid_rpc_config(
        PyramidXmlRPC, config.add_xmlrpc_endpoint, config.add_xmlrpc_method)
