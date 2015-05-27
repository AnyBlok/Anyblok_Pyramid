# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidDBTestCase
from anyblok import Declarations
from ..controllers import PyramidException
register = Declarations.register
PyramidXmlRPC = Declarations.PyramidXmlRPC
PyramidMixin = Declarations.PyramidMixin
Core = Declarations.Core


class TestDeclarationPyramidXmlRPC(PyramidDBTestCase):

    def check_controller(self):
        res = self.xmlrpc('/test', 'methodA', params=(2, 3))
        self.assertEqual(res, [4, 6])
        res = self.xmlrpc('/test', 'methodB', params=(2, 3))
        self.assertEqual(res, [6, 9])

    def test_xmlrpc(self):
        def add_xmlrpc_contoller():
            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return [x * 2 for x in args]

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_xmlrpc_without_route(self):
        def add_xmlrpc_contoller():

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return [x * 2 for x in args]

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

        with self.assertRaises(PyramidException):
            self.init_registry(add_xmlrpc_contoller)

    def test_simple_subclass_controller(self):
        def add_xmlrpc_contoller():

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)  # noqa
            class Test:

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_simple_subclass_base_xmlrpc(self):
        def add_xmlrpc_contoller():

            @register(Core)
            class PyramidBaseXmlRPC:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_simple_subclass_base_rpc(self):
        def add_xmlrpc_contoller():

            @register(Core)
            class PyramidBaseRPC:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_mixin_two_controller(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)
            class Test2(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test2, self).methodA(*args)

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')
            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test2, '/test2')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()
        res = self.xmlrpc('/test2', 'methodA', params=(2, 3))
        self.assertEqual(res, [4, 6])

    def test_mixin_one_controller_with_subclass(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidXmlRPC)
                class Test:

                    @PyramidXmlRPC.rpc_method(method='methodB')
                    def method_B(self, *args):
                        return [x * 3 for x in args]

            inherit_Test()

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_by_subclass_and_with(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidXmlRPC)
            class Test:

                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

            def inherit_Test():
                # put in the function else python take only on the first
                # Test class, because the fingerprint are the same
                @register(PyramidXmlRPC)
                class Test:

                    @PyramidXmlRPC.rpc_method(method='methodB')
                    def method_B(self, *args):
                        return super(Test, self).method_B(*args)

            inherit_Test()

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_mixin_one_controller_with_subclass_and_subclass_mixin(self):
        def add_xmlrpc_contoller():

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return None

            @register(PyramidXmlRPC)
            class Test:

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)  # noqa
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

            @register(PyramidMixin)  # noqa
            class PyMixin:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_inherit_by_another_controller(self):
        def add_xmlrpc_contoller():

            @register(PyramidXmlRPC)
            class Test2:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return [x * 2 for x in args]

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)
            class Test(PyramidXmlRPC.Test2):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return super(Test, self).method_B(*args)

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')
            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test2, '/test2')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_inherit_by_another_controller_and_subclass_maincontroller(self):
        def add_xmlrpc_contoller():

            @register(PyramidXmlRPC)
            class Test2:

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            @register(PyramidXmlRPC)
            class Test(PyramidXmlRPC.Test2):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return super(Test, self).method_B(*args)

            @register(PyramidXmlRPC)  # noqa
            class Test2:

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return [x * 2 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')
            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test2, '/test2')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()

    def test_inherit_core_and_mixin(self):
        def add_xmlrpc_contoller():

            @register(Core)
            class PyramidBaseRPC:

                def methodA(self, *args):
                    return [x * 2 for x in args]

            @register(PyramidMixin)
            class PyMixin:

                def methodA(self, *args):
                    return super(PyMixin, self).methodA(*args)

            @register(PyramidXmlRPC)
            class Test(PyramidMixin.PyMixin):

                @PyramidXmlRPC.rpc_method()
                def methodA(self, *args):
                    return super(Test, self).methodA(*args)

                @PyramidXmlRPC.rpc_method(method='methodB')
                def method_B(self, *args):
                    return [x * 3 for x in args]

            Declarations.PyramidXmlRPC.add_route(
                Declarations.PyramidXmlRPC.Test, '/test')

        self.init_registry(add_xmlrpc_contoller)
        self.check_controller()
