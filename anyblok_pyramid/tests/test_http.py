# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import anyblok_pyramid  # noqa
from anyblok.tests.testcase import TestCase
from anyblok.registry import RegistryManager
from anyblok.environment import EnvironmentManager
from anyblok import Declarations
register = Declarations.register
unregister = Declarations.unregister
PyramidHTTP = Declarations.PyramidHTTP


class OneController:
    pass


class TestPyramidHTTP(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPyramidHTTP, cls).setUpClass()
        RegistryManager.init_blok('testPyramidHTTP')
        EnvironmentManager.set('current_blok', 'testPyramidHTTP')
        cls.views = PyramidHTTP.views.copy()
        cls.routes = [] + PyramidHTTP.routes

    @classmethod
    def tearDownClass(cls):
        super(TestPyramidHTTP, cls).tearDownClass()
        EnvironmentManager.set('current_blok', None)
        del RegistryManager.loaded_bloks['testPyramidHTTP']
        PyramidHTTP.views = cls.views
        PyramidHTTP.routes = cls.routes

    def setUp(self):
        super(TestPyramidHTTP, self).setUp()
        blokname = 'testPyramidHTTP'
        RegistryManager.loaded_bloks[blokname]['PyramidHTTP'] = {
            'registry_names': []}

    def assertInPyramidHTTP(self, *args):
        blokname = 'testPyramidHTTP'
        blok = RegistryManager.loaded_bloks[blokname]
        bases = blok['PyramidHTTP']['PyramidHTTP.MyController']['bases']
        self.assertEqual(len(bases), len(args))
        for cls_ in args:
            has = cls_ in bases
            self.assertEqual(has, True)

    def assertInRemoved(self, cls):
        core = RegistryManager.loaded_bloks['testPyramidHTTP']['removed']
        if cls in core:
            return True

        self.fail('Not in removed')

    def test_add_interface(self):
        register(PyramidHTTP, cls_=OneController, name_='MyController')
        self.assertEqual('PyramidHTTP',
                         PyramidHTTP.MyController.__declaration_type__)
        self.assertInPyramidHTTP(OneController)
        dir(Declarations.PyramidHTTP.MyController)

    def test_add_interface_with_decorator(self):

        @register(PyramidHTTP)
        class MyController:
            pass

        self.assertEqual('PyramidHTTP',
                         PyramidHTTP.MyController.__declaration_type__)
        self.assertInPyramidHTTP(MyController)

    def test_add_two_interface(self):

        register(PyramidHTTP, cls_=OneController, name_="MyController")

        @register(PyramidHTTP)
        class MyController:
            pass

        self.assertInPyramidHTTP(OneController, MyController)

    def test_remove_interface_with_1_cls_in_registry(self):

        register(PyramidHTTP, cls_=OneController, name_="MyController")
        self.assertInPyramidHTTP(OneController)
        unregister(PyramidHTTP.MyController, OneController)
        self.assertInPyramidHTTP(OneController)
        self.assertInRemoved(OneController)

    def test_remove_interface_with_2_cls_in_registry(self):

        register(PyramidHTTP, cls_=OneController, name_="MyController")

        @register(PyramidHTTP)
        class MyController:
            pass

        self.assertInPyramidHTTP(OneController, MyController)
        unregister(PyramidHTTP.MyController, OneController)
        self.assertInPyramidHTTP(MyController, OneController)
        self.assertInRemoved(OneController)
