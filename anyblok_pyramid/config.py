from pyramid.config import Configurator
from anyblok.blok import BlokManager
from anyblok import Declarations
from os.path import join
from .handler import HandlerHTTP, HandlerRPC
from .controllers import Pyramid, PyramidHTTP, PyramidJsonRPC, PyramidXmlRPC


PyramidException = Declarations.Exception.PyramidException


def make_config():
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
    for route in Pyramid.routes:
        config.add_route(*route)

    for function, properties in Pyramid.views:
        config.add_view(function, **properties)


def pyramid_http_config(config):
    for route in PyramidHTTP.routes:
        config.add_route(*route)

    endpoints = [x[0] for x in PyramidHTTP.routes]
    for hargs, properties in PyramidHTTP.views.items():
        endpoint = '%s.%s' % hargs
        if endpoint not in endpoints:
            raise PyramidException(
                "One or more %s controller has been declared but no route have"
                " declared" % endpoint)
        config.add_view(HandlerHTTP(*hargs).wrap_view, **properties)


def _pyramid_rpc_config(cls, add_endpoint, add_method):
    for route in cls.routes:
        add_endpoint(*route)

    endpoints = [x[0] for x in cls.routes]
    for namespace in cls.methods:
        if namespace not in endpoints:
            raise PyramidException(
                "One or more %s controller has been declared but no route have"
                " declared" % namespace)
        for method in cls.methods[namespace]:
            rpc_method = cls.methods[namespace][method]
            rpc_method.pop('function')
            add_method(HandlerRPC(namespace, method).wrap_view,
                       route_name=namespace,
                       **rpc_method)


def pyramid_jsonrpc_config(config):
    _pyramid_rpc_config(
        PyramidJsonRPC, config.add_jsonrpc_endpoint, config.add_jsonrpc_method)


def pyramid_xmlrpc_config(config):
    _pyramid_rpc_config(
        PyramidXmlRPC, config.add_xmlrpc_endpoint, config.add_xmlrpc_method)
