from pyramid.config import Configurator
from anyblok.blok import BlokManager
from os.path import join
from .controllers import (pyramid_config,
                          pyramid_jsonrpc_config,
                          pyramid_xmlrpc_config)


def make_config():
    config = Configurator()
    config.include('pyramid_beaker')
    config.include('pyramid_rpc.jsonrpc')
    config.include('pyramid_rpc.xmlrpc')
    config.include(pyramid_config)
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
