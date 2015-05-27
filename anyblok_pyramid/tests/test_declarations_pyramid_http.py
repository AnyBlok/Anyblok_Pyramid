# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok import Declarations
from pyramid.response import Response
from ..controllers import PyramidException
from anyblok_pyramid.bloks.pyramid.exceptions import PyramidInvalidProperty
register = Declarations.register
PyramidHTTP = Declarations.PyramidHTTP
PyramidMixin = Declarations.PyramidMixin
Core = Declarations.Core


class TestDeclarationPyramidHTTP(PyramidDBTestCase):

    def check_controller(self):
        res = self.http('/test/methodA', params={'a': 2, 'b': 3})
        self.assertEqual(eval(res.body), {'a': 4, 'b': 6})
        res = self.http('/test/methodB', params={'a': 2, 'b': 3})
        self.assertEqual(eval(res.body), {'a': 6, 'b': 9})

    def add_routes(self):
        PyramidHTTP.add_route('methodA', '/test/methodA')
        PyramidHTTP.add_route('method_B', '/test/methodB')

    def add_routes2(self):
        PyramidHTTP.add_route('test2methodA', '/test2/methodA')
        PyramidHTTP.add_route('test2methodB', '/test2/methodB')

    def test_http(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def methodA(self, *args, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_http_without_routes(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

        with self.assertRaises(PyramidException):
            self.init_registry(add_http_contoller)

    def test_authentificated(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                @PyramidHTTP.authentificated()
                def methodA(self, *args, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_unknown_property(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                @PyramidHTTP.check_properties(unknown_property=True)
                def methodA(self, *args, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        with self.assertRaises(PyramidInvalidProperty):
            self.check_controller()

    def test_simple_subclass_controller(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)  # noqa
            class Test:

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_simple_subclass_base_http(self):
        def add_http_contoller():

            @register(Core)
            class PyramidBaseHTTP:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_mixin_one_controller(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_mixin_two_controller(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)
            class Test2(PyramidMixin.PyMixin):

                @PyramidHTTP.view(route_name='test2methodA')
                def methodA(self, **kwargs):
                    return Response(str(super(Test2, self).methodA(**kwargs)))

            self.add_routes()
            self.add_routes2()

        self.init_registry(add_http_contoller)
        self.check_controller()
        res = self.http('/test2/methodA', params={'a': 2, 'b': 3})
        self.assertEqual(eval(res.body), {'a': 4, 'b': 6})

    def test_mixin_one_controller_with_subclass(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidHTTP)
                class Test:

                    @PyramidHTTP.view()
                    def method_B(self, **kwargs):
                        return Response(str({x: int(y) * 3
                                             for x, y in kwargs.items()}))

            inherit_Test()

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass_and_with(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidHTTP)
            class Test:

                def method_B(self, **kwargs):
                    return {x: int(y) * 3 for x, y in kwargs.items()}

            @register(PyramidHTTP)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidHTTP)
                class Test:

                    @PyramidHTTP.view()
                    def method_B(self, **kwargs):
                        return Response(str(
                            super(Test, self).method_B(**kwargs)))

            inherit_Test()

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_mixin_one_controller_with_subclass_and_subclass_mixin(self):
        def add_http_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return None

            @register(PyramidHTTP)
            class Test:

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

            @register(PyramidMixin)  # noqa
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_inherit_by_another_controller(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test2:

                @PyramidHTTP.view(route_name='test2methodA')
                def methodA(self, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

                @PyramidHTTP.view(route_name='test2methodB')
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)
            class Test(PyramidHTTP.Test2):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return super(Test, self).method_B(**kwargs)

            self.add_routes()
            self.add_routes2()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_inherit_by_another_controller_and_subclass_maincontroller(self):
        def add_http_contoller():

            @register(PyramidHTTP)
            class Test2:

                @PyramidHTTP.view(route_name='test2methodB')
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            @register(PyramidHTTP)
            class Test(PyramidHTTP.Test2):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return super(Test, self).method_B(**kwargs)

            @register(PyramidHTTP)  # noqa
            class Test2:

                @PyramidHTTP.view(route_name='test2methodA')
                def methodA(self, **kwargs):
                    return Response(str({x: int(y) * 2
                                         for x, y in kwargs.items()}))

            self.add_routes()
            self.add_routes2()

        self.init_registry(add_http_contoller)
        self.check_controller()

    def test_inherit_core_and_mixin(self):
        def add_http_contoller():

            @register(Core)
            class PyramidBase:

                def methodA(self, **kwargs):
                    return {x: int(y) * 2 for x, y in kwargs.items()}

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return super(PyMixin, self).methodA(**kwargs)

            @register(PyramidHTTP)
            class Test(PyramidMixin.PyMixin):

                @PyramidHTTP.view()
                def methodA(self, **kwargs):
                    return Response(str(super(Test, self).methodA(**kwargs)))

                @PyramidHTTP.view()
                def method_B(self, **kwargs):
                    return Response(str({x: int(y) * 3
                                         for x, y in kwargs.items()}))

            self.add_routes()

        self.init_registry(add_http_contoller)
        self.check_controller()
