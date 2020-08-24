# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.authentication import (
    AuthTktAuthenticationPolicy,
    RemoteUserAuthenticationPolicy,
    SessionAuthenticationPolicy,
    BasicAuthAuthenticationPolicy,
)
from anyblok.config import Configuration


def getAuthenticationPolicy():
    """Return the authentication policy set in configuration
    """
    method = Configuration.get('pyramid_authentication_method')
    if method is AuthTktAuthenticationPolicy:
        return getAuthTktAuthenticationPolicy()
    if method is RemoteUserAuthenticationPolicy:
        return getRemoteUserAuthenticationPolicy()
    if method is SessionAuthenticationPolicy:
        return getSessionAuthenticationPolicy()
    if method is BasicAuthAuthenticationPolicy:
        return getBasicAuthAuthenticationPolicy()

    return method()


def getAuthTktAuthenticationPolicy():
    """Define the authentication policy for Tkt"""
    return AuthTktAuthenticationPolicy(
        Configuration.get('pyramid_authtkt_secret'),
        callback=Configuration.get('pyramid_authentication_callback'),
        cookie_name=Configuration.get('pyramid_authtkt_cookie_name'),
        secure=Configuration.get('pyramid_authtkt_secure'),
        http_only=Configuration.get('pyramid_authtkt_http_only'),
        timeout=Configuration.get('pyramid_authtkt_timeout'),
        max_age=Configuration.get('pyramid_authtkt_max_age'),
        debug=Configuration.get('pyramid_authentication_debug')
    )


def getRemoteUserAuthenticationPolicy():
    """Define the authentication policy for remote user server"""
    return RemoteUserAuthenticationPolicy(
        environ_key=Configuration.get('pyramid_remoteuser_environ_key'),
        callback=Configuration.get('pyramid_authentication_callback'),
        debug=Configuration.get('pyramid_authentication_debug')
    )


def getSessionAuthenticationPolicy():
    """Define the session based authentication policy"""
    return SessionAuthenticationPolicy(
        prefix=Configuration.get('pyramid_session_prefix'),
        callback=Configuration.get('pyramid_authentication_callback'),
        debug=Configuration.get('pyramid_authentication_debug')
    )


def getBasicAuthAuthenticationPolicy():
    """Define basic auth authentication policy"""
    return BasicAuthAuthenticationPolicy(
        Configuration.get('pyramid_basicauth_check'),
        debug=Configuration.get('pyramid_authentication_debug')
    )
