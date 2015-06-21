# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration
from anyblok.registry import RegistryManager
from anyblok.tests.testcase import DBTestCase, BlokTestCase
from webtest import TestApp
from ..config import make_config
from pyramid.response import Response
import json
from pyramid_rpc.compat import xmlrpclib


class PyramidTestCase:

    @classmethod
    def setUpClass(cls):
        super(PyramidTestCase, cls).setUpClass()
        RegistryManager.add_needed_bloks('pyramid')

    def http(self, path, params=None, method='post'):
        resp = getattr(self.webserver, method)(path, params)
        self.assertEqual(resp.status_int, 200)
        return resp

    def jsonrpc(self, path, method, params=None):
        body = {
            'id': 5,
            'jsonrpc': '2.0',
            'method': method,
        }
        if params is not None:
            body['params'] = params

        kwargs = dict(content_type='application/json', params=json.dumps(body))
        resp = self.webserver.post(path, **kwargs)
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.content_type, 'application/json')
        result = resp.json
        self.assertEqual(result['jsonrpc'], '2.0')
        self.assertEqual(result['id'], 5)
        return result

    def xmlrpc(self, path, method, params=None):
        if params is None:
            params = tuple()

        xml = xmlrpclib.dumps(params, methodname=method).encode('utf-8')
        resp = self.webserver.post(path, content_type='text/xml', params=xml)
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.content_type, 'text/xml')
        return xmlrpclib.loads(resp.body)[0][0]

    def init_web_server(self):
        config = make_config()
        app = config.make_wsgi_app()
        self.webserver = TestApp(app)
        dbname = Configuration.get('db_name')
        if dbname is None:
            dbname = 'test_anyblok'

        self.webserver.post('/pyramid/testcase/database?database=%s' % dbname)


class PyramidDBTestCase(PyramidTestCase, DBTestCase):

    def init_registry(self, function, **kwargs):
        from anyblok import Declarations
        pyramid_routes = [] + Declarations.Pyramid.routes
        pyramid_views = [] + Declarations.Pyramid.views
        pyramid_http_routes = [] + Declarations.PyramidHTTP.routes
        pyramid_http_views = Declarations.PyramidHTTP.views.copy()
        pyramid_jsonrpc_routes = [] + Declarations.PyramidJsonRPC.routes
        pyramid_jsonrpc_methods = Declarations.PyramidJsonRPC.methods.copy()
        pyramid_xmlrpc_routes = [] + Declarations.PyramidXmlRPC.routes
        pyramid_xmlrpc_methods = Declarations.PyramidXmlRPC.methods.copy()

        def wrap_fnct(**wfkwargs):
            Declarations.Pyramid.add_route(
                'pyramidtestcasedatabase', '/pyramid/testcase/database')

            @Declarations.Pyramid.add_view('pyramidtestcasedatabase',
                                           request_method='POST')
            def save_db_in_session(request, database=None):
                request.session['database'] = database
                request.session.save()
                return Response('ok')

            function(**wfkwargs)

        try:
            res = super(PyramidDBTestCase, self).init_registry(wrap_fnct,
                                                               **kwargs)
            self.init_web_server()
        finally:
            Declarations.Pyramid.routes = pyramid_routes
            Declarations.Pyramid.views = pyramid_views
            Declarations.PyramidHTTP.routes = pyramid_http_routes
            Declarations.PyramidHTTP.views = pyramid_http_views
            Declarations.PyramidJsonRPC.routes = pyramid_jsonrpc_routes
            Declarations.PyramidJsonRPC.methods = pyramid_jsonrpc_methods
            Declarations.PyramidXmlRPC.routes = pyramid_xmlrpc_routes
            Declarations.PyramidXmlRPC.methods = pyramid_xmlrpc_methods

        return res


class PyramidBlokTestCase(PyramidTestCase, BlokTestCase):

    def setUp(self):
        super(PyramidBlokTestCase, self).setUp()
        self.init_web_server()
