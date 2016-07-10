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


Add route, view, ... in pyramid config
--------------------------------------

By includeme
~~~~~~~~~~~~

1. define the view in one file

  in the file views.py::

      from pyramid.view import view_config
      from pyramid.response import Response

      @view_config(route_name='hello')
      def say_hello(request):
          return Response('Hello %(name)s !!!' % request.matchdict)

2. define the entrypoint function

   in the file foo.py::

       def update_pyramid_config(config):
           config.add_route('hello', '/hello/{name})
           config.scan('.views')


By blok
~~~~~~~

1. define the view in one file of the blok

  in the file views.py::

      from pyramid.view import view_config
      from pyramid.response import Response

      @view_config(route_name='hello')
      def say_hello(request):
          return Response('Hello %(name)s !!!' % request.matchdict)

2. add the class method ``pyramid_load_config``

   in the file foo.py::

       from anyblok.blok import Blok

       class MyBlok(Blok):

           ...

           @classmethod
           def pyramid_load_config(cls, config):
               config.add_route('hello', '/hello/{name}')
               config.scan(cls.__module__ + '.views')


Get AnyBlok registry in view
----------------------------

By default the registry load is the registry of the ``Configuration`` ``db_name``
key.

Define a simple view::

    from pyramid.view import view_config
    from pyramid.response import Response


    @view_config(route_name='foo')
    def bar(request):
        registry = request.anyblok.registry
        nb_installed_bloks = registry.System.Blok.query().filter_by(
            state='installed').count()
        return Response("Welcome in AnyBlok application, you have %d installed "
                        "bloks" % nb_installed_bloks)


Define view which are used only if one blok is installed
--------------------------------------------------------

See the link `view and route predicated <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#adding-a-third-party-view-route-or-subscriber-predicate>`_

the goal of the prédicate is to get the access of the route or the view only if
the predicate condition is validated. AnyBlok / Pyramid add the predicate
``installed_blok``::

    from pyramid.view import view_config
    from pyramid.response import Response


    @view_config(route_name='foo')
    def bar1(request):
        """ This is the default view """
        return Response("Welcome in AnyBlok application, you have 0 installed "
                        "bloks")

    @view_config(route_name='foo', installed_blok='anyblok-core')
    def bar2(request):
        """ This view id call if the anyblok is installed """
        registry = request.anyblok.registry
        nb_installed_bloks = registry.System.Blok.query().filter_by(
            state='installed').count()
        return Response("Welcome in AnyBlok application, you have %d installed "
                        "bloks" % nb_installed_bloks)


.. note::

    Installed predicated detect if the registry is load, without registry,
    the installated blok can no be verify.


.. note::

    you can use the ``current_blok`` function to not write the blok name::

        from anyblok_pyramid import current_blok

        @view_config(route_name='foo', installed_blok=current_blok())
        def bar2(request):
            """ This view id call if the anyblok is installed """
            registry = request.anyblok.registry
            nb_installed_bloks = registry.System.Blok.query().filter_by(
                state='installed').count()
            return Response("Welcome in AnyBlok application, you have %d installed "
                            "bloks" % nb_installed_bloks)

Define the name of the database
-------------------------------

The name of the database determine the registry use by the view.

By default the name of the database come from the ``Configuration`` ``db_name``
key. But it is possible to define a callback to define the good db name.

Define an AnyBlok init function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the setup of the package add new entry point::

    setup(
        ...
        entry_points={
            ...
            'anyblok.init': ['get_db_name=package.path:add_get_db_name'],
            ...
        },
        ...
    )

In the file ``path`` of the ``package`` add the method ``add_get_db_name``::

    def add_get_db_name():
        from anyblok.config import Configuration

        def get_db_name(request):
            return ``My db Name``

        @Configuration.add('plugins'):
        def update_plugins(group):
            group.set_defaults(get_db_name=get_db_name)


Define the db name in the request path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is an example to define the good db name in function of the path of the
method.

This example work if the path id define like this::

    config.add_route('one_route', '/{dbname}/foo/bar')


The definition of ``get_db_name`` is::

    def add_get_db_name():
        from anyblok.config import Configuration

        def get_db_name(request):
            return request.matchdict.get(
                dbname',
                Configuration.get('db_name'))

        @Configuration.add('plugins'):
        def update_plugins(group):
            group.set_defaults(get_db_name=get_db_name)



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
