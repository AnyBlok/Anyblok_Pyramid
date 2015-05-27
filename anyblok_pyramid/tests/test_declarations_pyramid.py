# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from pyramid.response import Response
from webtest import AppError


class TestDeclarationPyramid(PyramidDBTestCase):
    def add_in_registry(self, path=None):
        from anyblok import Declarations
        Pyramid = Declarations.Pyramid

        @Pyramid.add_view('MyView')
        def my_view(request, **kwargs):
            return Response(str(kwargs))

        Pyramid.add_route('MyView', pattern=path)

    def test_add_view(self):
        path = '/test/add/view'
        self.init_registry(self.add_in_registry, path=path)
        response = self.webserver.get(path)
        self.assertEqual(response.status, '200 OK')

    def test_param(self):
        path = '/test/add/view/'
        self.init_registry(self.add_in_registry, path=path + '{name}')
        response = self.webserver.get(path + 'AnyBlok')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(eval(response.body), {'name': 'AnyBlok'})

    def test_argument(self):
        path = '/test/add/view'
        self.init_registry(self.add_in_registry, path=path)
        response = self.webserver.get(path + '?name=AnyBlok')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(eval(response.body), {'name': 'AnyBlok'})

    def add_in_registry_rest(self, path=None, request_method='GET'):
        from anyblok import Declarations
        Pyramid = Declarations.Pyramid

        @Pyramid.add_view('MyView', request_method=request_method)
        def my_view(request):
            return Response(request_method)

        Pyramid.add_route('MyView', path)

    def test_REst_get(self):
        path = '/test/rest/get'
        self.init_registry(self.add_in_registry_rest, path=path)
        response = self.webserver.get(path)
        self.assertEqual(response.status, '200 OK')
        for request_method in ('put', 'post', 'delete'):
            try:
                getattr(self.webserver, request_method)(path)
                self.fail('%r are not allowed for this path %r' % (
                    request_method, path))
            except AppError as e:
                if '404' not in e.args[0]:
                    raise

    def test_REst_put(self):
        path = '/test/rest/put'
        self.init_registry(self.add_in_registry_rest, path=path,
                           request_method='PUT')
        response = self.webserver.put(path)
        self.assertEqual(response.status, '200 OK')
        for request_method in ('get', 'post', 'delete'):
            try:
                getattr(self.webserver, request_method)(path)
                self.fail('%r are not allowed for this path %r' % (
                    request_method, path))
            except AppError as e:
                if '404' not in e.args[0]:
                    raise

    def test_REst_post(self):
        path = '/test/rest/post'
        self.init_registry(self.add_in_registry_rest, path=path,
                           request_method='POST')
        response = self.webserver.post(path)
        self.assertEqual(response.status, '200 OK')
        for request_method in ('get', 'put', 'delete'):
            try:
                getattr(self.webserver, request_method)(path)
                self.fail('%r are not allowed for this path %r' % (
                    request_method, path))
            except AppError as e:
                if '404' not in e.args[0]:
                    raise

    def test_REst_delete(self):
        path = '/test/rest/delete'
        self.init_registry(self.add_in_registry_rest, path=path,
                           request_method='DELETE')
        response = self.webserver.delete(path)
        self.assertEqual(response.status, '200 OK')
        for request_method in ('get', 'put', 'post'):
            try:
                getattr(self.webserver, request_method)(path)
                self.fail('%r are not allowed for this path %r' % (
                    request_method, path))
            except AppError as e:
                if '404' not in e.args[0]:
                    raise
