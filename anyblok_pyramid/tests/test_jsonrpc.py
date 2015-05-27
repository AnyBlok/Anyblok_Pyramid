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
PyramidJsonRPC = Declarations.PyramidJsonRPC


class OneController:
    pass


class TestPyramidJsonRPC(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPyramidJsonRPC, cls).setUpClass()
        RegistryManager.init_blok('testPyramidJsonRPC')
        EnvironmentManager.set('current_blok', 'testPyramidJsonRPC')
        cls.methods = PyramidJsonRPC.methods.copy()
        cls.routes = [] + PyramidJsonRPC.routes

    @classmethod
    def tearDownClass(cls):
        super(TestPyramidJsonRPC, cls).tearDownClass()
        EnvironmentManager.set('current_blok', None)
        del RegistryManager.loaded_bloks['testPyramidJsonRPC']
        PyramidJsonRPC.methods = cls.methods
        PyramidJsonRPC.routes = cls.routes

    def setUp(self):
        super(TestPyramidJsonRPC, self).setUp()
        blokname = 'testPyramidJsonRPC'
        RegistryManager.loaded_bloks[blokname]['PyramidJsonRPC'] = {
            'registry_names': []}

    def assertInPyramidJsonRPC(self, *args):
        blokname = 'testPyramidJsonRPC'
        blok = RegistryManager.loaded_bloks[blokname]
        bases = blok['PyramidJsonRPC']['PyramidJsonRPC.MyController']['bases']
        self.assertEqual(len(bases), len(args))
        for cls_ in args:
            has = cls_ in bases
            self.assertEqual(has, True)

    def assertInRemoved(self, cls):
        core = RegistryManager.loaded_bloks['testPyramidJsonRPC']['removed']
        if cls in core:
            return True

        self.fail('Not in removed')

    def test_add_interface(self):
        register(PyramidJsonRPC, cls_=OneController, name_='MyController')
        self.assertEqual('PyramidJsonRPC',
                         PyramidJsonRPC.MyController.__declaration_type__)
        self.assertInPyramidJsonRPC(OneController)
        dir(Declarations.PyramidJsonRPC.MyController)

    def test_add_interface_with_decorator(self):

        @register(PyramidJsonRPC)
        class MyController:
            pass

        self.assertEqual('PyramidJsonRPC',
                         PyramidJsonRPC.MyController.__declaration_type__)
        self.assertInPyramidJsonRPC(MyController)

    def test_add_two_interface(self):

        register(PyramidJsonRPC, cls_=OneController, name_="MyController")

        @register(PyramidJsonRPC)
        class MyController:
            pass

        self.assertInPyramidJsonRPC(OneController, MyController)

    def test_remove_interface_with_1_cls_in_registry(self):

        register(PyramidJsonRPC, cls_=OneController, name_="MyController")
        self.assertInPyramidJsonRPC(OneController)
        unregister(PyramidJsonRPC.MyController, OneController)
        self.assertInPyramidJsonRPC(OneController)
        self.assertInRemoved(OneController)

    def test_remove_interface_with_2_cls_in_registry(self):

        register(PyramidJsonRPC, cls_=OneController, name_="MyController")

        @register(PyramidJsonRPC)
        class MyController:
            pass

        self.assertInPyramidJsonRPC(OneController, MyController)
        unregister(PyramidJsonRPC.MyController, OneController)
        self.assertInPyramidJsonRPC(MyController, OneController)
        self.assertInRemoved(OneController)
