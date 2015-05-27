# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from ..controllers import PyramidException
from anyblok import Declarations
register = Declarations.register
PyramidJsonRPC = Declarations.PyramidJsonRPC
PyramidMixin = Declarations.PyramidMixin
Core = Declarations.Core


class TestDeclarationPyramidJsonRPC(PyramidDBTestCase):

    def check_controller(self):
        res = self.jsonrpc('/test', 'methodA', params={'a': 2, 'b': 3})
        self.assertEqual(res['result'], {'a': 4, 'b': 6})
        res = self.jsonrpc('/test', 'methodB', params={'a': 2, 'b': 3})
        self.assertEqual(res['result'], {'a': 6, 'b': 9})

    def test_jsonrpc(self):
        def add_jsonrpc_contoller():

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_jsonrpc_without_routes(self):
        def add_jsonrpc_contoller():

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

        with self.assertRaises(PyramidException):
            self.init_registry(add_jsonrpc_contoller)

    def test_simple_subclass_controller(self):
        def add_jsonrpc_contoller():

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)  # noqa
            class Test:

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_simple_subclass_base_jsonrpc(self):
        def add_jsonrpc_contoller():

            @register(Core)
            class PyramidBaseJsonRPC:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_simple_subclass_base_rpc(self):
        def add_jsonrpc_contoller():

            @register(Core)
            class PyramidBaseRPC:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_mixin_two_controller(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test2(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test2, self).methodA(**kwargs)

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')
            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test2, '/test2')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()
        res = self.jsonrpc('/test2', 'methodA', params={'a': 2, 'b': 3})
        self.assertEqual(res['result'], {'a': 4, 'b': 6})

    def test_mixin_one_controller_with_subclass(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidJsonRPC)
                class Test:

                    @PyramidJsonRPC.rpc_method(method='methodB')
                    def method_B(self, **kwargs):
                        return {x: y * 3 for x, y in kwargs.items()}

            inherit_Test()

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass_and_with(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test:

                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidJsonRPC)
                class Test:

                    @PyramidJsonRPC.rpc_method(method='methodB')
                    def method_B(self, **kwargs):
                        return super(Test, self).method_B(**kwargs)

            inherit_Test()

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_with_subclass_and_subclass_mixin(self):
        def add_jsonrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return None

            @register(PyramidJsonRPC)
            class Test:

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

            @register(PyramidMixin)  # noqa
            class PyMixin:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_inherit_by_another_controller(self):
        def add_jsonrpc_contoller():

            @register(PyramidJsonRPC)
            class Test2:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test(PyramidJsonRPC.Test2):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return super(Test, self).method_B(**kwargs)

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')
            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test2, '/test2')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_inherit_by_another_controller_and_subclass_maincontroller(self):
        def add_jsonrpc_contoller():

            @register(PyramidJsonRPC)
            class Test2:

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            @register(PyramidJsonRPC)
            class Test(PyramidJsonRPC.Test2):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return super(Test, self).method_B(**kwargs)

            @register(PyramidJsonRPC)  # noqa
            class Test2:

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')
            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test2, '/test2')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()

    def test_inherit_core_and_mixin(self):
        def add_jsonrpc_contoller():

            @register(Core)
            class PyramidBaseRPC:

                def methodA(self, **kwargs):
                    return {x: y * 2 for x, y in kwargs.items()}

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, **kwargs):
                    return super(PyMixin, self).methodA(**kwargs)

            @register(PyramidJsonRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidJsonRPC.rpc_method()
                def methodA(self, **kwargs):
                    return super(Test, self).methodA(**kwargs)

                @PyramidJsonRPC.rpc_method(method='methodB')
                def method_B(self, **kwargs):
                    return {x: y * 3 for x, y in kwargs.items()}

            Declarations.PyramidJsonRPC.add_route(
                Declarations.PyramidJsonRPC.Test, '/test')

        self.init_registry(add_jsonrpc_contoller)
        self.check_controller()
