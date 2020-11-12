# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2002 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_pyramid.security import AnyBlokResourceFactory
from anyblok_pyramid.bloks.auth.views import login, logout
from anyblok_pyramid.bloks.pyramid.oidc import (
    login as oidc_login,
    callback as oidc_callback,
)


class Test(Blok):

    version = "1.0.0"
    required = ["auth"]

    @classmethod
    def import_declaration_module(cls):
        from . import models  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import models

        reload(models)

    @classmethod
    def pyramid_load_config(cls, config):
        config.add_route(
            "bloks",
            "/bloks",
            factory=AnyBlokResourceFactory("Model.System.Blok"),
        )
        config.add_route(
            "blok",
            "/blok/{name}",
            factory=AnyBlokResourceFactory("Model.System.Blok"),
        )
        config.add_route("login", "/login", request_method="POST")
        config.add_view(view=login, route_name="login", renderer="JSON")
        config.add_route("logout", "/logout", request_method="POST")
        config.add_view(view=logout, route_name="logout")

        config.add_route("oidc_login", "/oidc_login", request_method="GET")
        config.add_view(view=oidc_login, route_name="oidc_login")
        config.add_route(
            "oidc_callback", "/oidc_callback", request_method="GET"
        )
        config.add_view(view=oidc_callback, route_name="oidc_callback")

        config.scan(cls.__module__ + ".views")

    def update(self, latest):
        if not latest:
            self.registry.Pyramid.User.insert(login="admin")
            self.registry.Pyramid.User.insert(login="viewer")
            self.registry.Pyramid.User.insert(login="user@anyblok.org")
            self.registry.Pyramid.User.insert(login="user2@anyblok.org")
