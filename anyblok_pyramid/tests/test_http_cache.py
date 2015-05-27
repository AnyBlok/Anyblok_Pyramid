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
register = Declarations.register
PyramidHTTP = Declarations.PyramidHTTP
PyramidMixin = Declarations.PyramidMixin
Core = Declarations.Core


class TestSimpleCache(PyramidDBTestCase):

    def call_http(self, value):
        res = self.http('/test', method='get')
        self.assertEqual(eval(res.body), value)

    def check_method_cached(self, registry, registry_name, value=1):
        self.call_http(value)
        self.call_http(value)
        registry.System.Cache.invalidate(registry_name, 'method_cached')
        self.call_http(value * 2)

    def add_controller(self):
        @register(PyramidHTTP)
        class Test:

            @PyramidHTTP.view()
            def get_method_cached(self):
                return Response(str(self.method_cached()))

        PyramidHTTP.add_route('get_method_cached', '/test')

    def test_model(self):
        def add_model_with_method_cached():

            @register(PyramidHTTP)
            class Test:

                x = 0

                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.x += 1
                    return cls.x

            self.add_controller()

        registry = self.init_registry(add_model_with_method_cached)
        self.check_method_cached(registry, 'PyramidHTTP.Test')

    def test_core(self):
        def add_model_with_method_cached_by_core():
            @register(Core)
            class PyramidBaseHTTP:

                x = 0

                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.x += 1
                    return cls.x

            self.add_controller()

        registry = self.init_registry(add_model_with_method_cached_by_core)
        self.check_method_cached(registry, 'PyramidHTTP.Test')

    def test_mixin(self):
        def add_model_with_method_cached_by_mixin():
            @register(PyramidMixin)
            class MTest:

                x = 0

                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.x += 1
                    return cls.x

            @register(PyramidHTTP)
            class Test(PyramidMixin.MTest):
                pass

            self.add_controller()

        registry = self.init_registry(add_model_with_method_cached_by_mixin)
        self.check_method_cached(registry, 'PyramidHTTP.Test')

    def add_model_with_method_cached_with_mixin_and_or_core(self,
                                                            withmodel=False,
                                                            withmixin=False,
                                                            withcore=False):

        @register(Core)
        class PyramidBaseHTTP:

            x = 0

            if withcore:
                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.x += 1
                    return cls.x

            else:
                @classmethod
                def method_cached(cls):
                    cls.x += 1
                    return cls.x

        @register(PyramidMixin)
        class MTest:

            y = 0

            if withmixin:
                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(MTest, cls).method_cached()

            else:
                @classmethod
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(MTest, cls).method_cached()

        @register(PyramidHTTP)
        class Test(PyramidMixin.MTest):

            z = 0

            if withmodel:
                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.z += 3
                    return cls.z + super(Test, cls).method_cached()
            else:
                @classmethod
                def method_cached(cls):
                    cls.z += 3
                    return cls.z + super(Test, cls).method_cached()

        self.add_controller()

    def test_model_mixin_core_not_cache(self):
        self.init_registry(
            self.add_model_with_method_cached_with_mixin_and_or_core)
        self.call_http(6)
        self.call_http(12)

    def test_model_mixin_core_only_core(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_with_mixin_and_or_core,
            withcore=True)
        self.call_http(6)
        self.call_http(11)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(17)

    def test_model_mixin_core_only_mixin(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_with_mixin_and_or_core,
            withmixin=True)
        self.call_http(6)
        self.call_http(9)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(15)

    def test_model_mixin_core_only_model(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_with_mixin_and_or_core,
            withmodel=True)
        self.call_http(6)
        self.call_http(6)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(12)

    def test_model_mixin_core_only_core_and_mixin(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_with_mixin_and_or_core,
            withmixin=True, withcore=True)
        self.call_http(6)
        self.call_http(9)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(15)


class TestInheritedCache(PyramidDBTestCase):

    def call_http(self, value):
        res = self.http('/test', method='get')
        self.assertEqual(eval(res.body), value)

    def check_method_cached(self, registry):
        self.call_http(3)
        self.call_http(5)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(8)

    def check_inherited_method_cached(self, registry):
        self.call_http(3)
        self.call_http(3)
        registry.System.Cache.invalidate('PyramidHTTP.Test',
                                         'method_cached')
        self.call_http(6)

    def add_controller(self):
        @register(PyramidHTTP)
        class Test:

            @PyramidHTTP.view()
            def get_method_cached(self):
                return Response(str(self.method_cached()))

        PyramidHTTP.add_route('get_method_cached', '/test')

    def add_model_with_method_cached(self, inheritcache=False):

        @register(PyramidHTTP)
        class Test:

            x = 0

            @Declarations.classmethod_cache()
            def method_cached(cls):
                cls.x += 1
                return cls.x

        @register(PyramidHTTP)  # noqa
        class Test:

            y = 0

            if inheritcache:
                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(Test, cls).method_cached()
            else:
                @classmethod
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(Test, cls).method_cached()

        self.add_controller()

    def add_model_with_method_cached_by_core(self, inheritcache=False):

        @register(Core)
        class PyramidBaseHTTP:

            x = 0

            @Declarations.classmethod_cache()
            def method_cached(cls):
                cls.x += 1
                return cls.x

        @register(Core)  # noqa
        class PyramidBaseHTTP:

            y = 0

            if inheritcache:
                @Declarations.classmethod_cache()
                def method_cached(self):
                    self.y += 2
                    return self.y + super(PyramidBaseHTTP,
                                          self).method_cached()
            else:
                @classmethod
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(PyramidBaseHTTP, cls).method_cached()

        self.add_controller()

    def add_model_with_method_cached_by_mixin(self, inheritcache=False):

        @register(PyramidMixin)
        class MTest:

            x = 0

            @Declarations.classmethod_cache()
            def method_cached(cls):
                cls.x += 1
                return cls.x

        @register(PyramidMixin)  # noqa
        class MTest:

            y = 0

            if inheritcache:
                @Declarations.classmethod_cache()
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(MTest, cls).method_cached()
            else:
                @classmethod
                def method_cached(cls):
                    cls.y += 2
                    return cls.y + super(MTest, cls).method_cached()

        @register(PyramidHTTP)
        class Test(PyramidMixin.MTest):
            pass

        self.add_controller()

    def test_model(self):
        registry = self.init_registry(self.add_model_with_method_cached)
        self.check_method_cached(registry)

    def test_model2(self):
        registry = self.init_registry(self.add_model_with_method_cached,
                                      inheritcache=True)
        self.check_inherited_method_cached(registry)

    def test_core(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_by_core)
        self.check_method_cached(registry)

    def test_core2(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_by_core, inheritcache=True)
        self.check_inherited_method_cached(registry)

    def test_mixin(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_by_mixin)
        self.check_method_cached(registry)

    def test_mixin2(self):
        registry = self.init_registry(
            self.add_model_with_method_cached_by_mixin, inheritcache=True)
        self.check_inherited_method_cached(registry)
