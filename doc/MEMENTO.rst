.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

MEMENTO
=======

Anyblok / Pyramid mainly depends on:

* Python 3.3+
* `AnyBlok <http://doc.anyblok.org>`_
* `Pyramid <http://pyramid.readthedocs.org>`_


WorkingSet
----------

Anyblok / Pyramid add two function to use callback:

* `set_callable`: save a callback, the name of the callable is the name of the callback
* `get_callable`: return a callback in function of this name

for exemple, see the callable `get_registry`::

    registry = get_callable('get_registry')(request)

Authentication and authorization
--------------------------------

Authentication can be add directly in configuration with includeme.

Links to the official documentation :

* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/design.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authorization.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authentication.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/quick_tutorial/authorization.html
* http://docs.pylonsproject.org/projects/pyramid//en/latest/quick_tutorial/authentication.html

Link to an official tutorial
If you want to replace default pyramid component by your own:

* http://docs.pylonsproject.org/projects/pyramid//en/latest/narr/security.html#creating-your-own-authentication-policy
* http://docs.pylonsproject.org/projects/pyramid//en/latest/narr/security.html#creating-your-own-authorization-policy

Add a root factory::

    class RootFactory(object):

        def __init__(self, request):
            self.request = request

        __acl__ = [
            (Allow, Everyone, 'all'),
        ]

Add the authentication callback::

    def group_finder(email, request):
        return ("all",)

Add the includeme callable::

    def pyramid_security_config(config):
        # Authentication policy
        secret = Configuration.get("authn_key", "secret")
        authn_policy = AuthTktAuthenticationPolicy(secret=secret,
                                                   callback=group_finder)
        config.set_authentication_policy(authn_policy)
        # Authorization policy
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
        # Root factory: only added if set in config file (no default one)
        config.set_root_factory(RootFactory)

Add the includeme in the entry point::

        setup(
            ...,
            entry_points={
                'anyblok_pyramid.includeme': [
                    'pyramid_security_config=path:pyramid_security_config',
                    ...
                ],
            },
            ...,
        )

.. note::

    You can get the session, with the callback get_registry::

        from anyblok_pyramid import get_callable
        # only if get_registry is implemented for you use case
        registry = get_callable('get_registry')(request)

.. note::

    You can merge the authorization of Pyramid and the authorization of AnyBlok

JSON adapter
------------

In the case where you need to return json value you can format the data with:

* Define an adapter for the python ``type``::

    def datetime_adapter(obj, request):
        return obj.isoformat()

* Add the adapter at the pyramid configuration::

    def declare_json_data_adapter(config):
        from pyramid.renderers import JSON
        json_renderer = JSON()
        json_renderer.add_adapter(datetime, datetime_adapter)
        config.add_renderer('json', json_renderer)

* Add the includeme::

    setup(
        ...,
        entry_points={
            'anyblok_pyramid.includeme': [
                'json_adapter=path:declare_json_data_adapter',
                ...
            ],
        },
        ...,
    )
