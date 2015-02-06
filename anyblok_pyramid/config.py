# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.config import Configurator
from anyblok.blok import BlokManager
from anyblok import Declarations
from os.path import join
from .handler import HandlerHTTP, HandlerRPC
from .controllers import Pyramid, PyramidHTTP, PyramidJsonRPC, PyramidXmlRPC


PyramidException = Declarations.Exception.PyramidException


def make_config():
    """ Return the configuration for pyramid """
    config = Configurator()
    config.include('pyramid_beaker')
    config.include('pyramid_rpc.jsonrpc')
    config.include('pyramid_rpc.xmlrpc')
    config.include(pyramid_config)
    config.include(pyramid_http_config)
    config.include(pyramid_jsonrpc_config)
    config.include(pyramid_xmlrpc_config)
    config.include(declare_static)
    return config


def declare_static(config):
    """ Pyramid includeme, add the static path of the blok

    :param config: the pyramid configuration
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
    """ Pyramid includeme, add the route and view which are not
    added in the blok

    :param config: the pyramid configuration
    """
    for args, kwargs in Pyramid.routes:
        config.add_route(*args, **kwargs)

    for function, properties in Pyramid.views:
        config.add_view(function, **properties)


def pyramid_http_config(config):
    """ Pyramid includeme, add the route and view which are
    added in the blok by ``PyramidHTTP`` Type

    :param config: the pyramid configuration
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
    """ Pyramid includeme, add the route and view which are
    added in the blok by ``PyramidJsonRPC`` Type

    :param config: the pyramid configuration
    """
    _pyramid_rpc_config(
        PyramidJsonRPC, config.add_jsonrpc_endpoint, config.add_jsonrpc_method)


def pyramid_xmlrpc_config(config):
    """ Pyramid includeme, add the route and view which are
    added in the blok by ``PyramidXmlRPC`` Type

    :param config: the pyramid configuration
    """
    _pyramid_rpc_config(
        PyramidXmlRPC, config.add_xmlrpc_endpoint, config.add_xmlrpc_method)
