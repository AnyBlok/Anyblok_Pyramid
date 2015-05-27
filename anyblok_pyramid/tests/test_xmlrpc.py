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
PyramidXmlRPC = Declarations.PyramidXmlRPC


class OneController:
    pass


class TestPyramidXmlRPC(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPyramidXmlRPC, cls).setUpClass()
        RegistryManager.init_blok('testPyramidXmlRPC')
        EnvironmentManager.set('current_blok', 'testPyramidXmlRPC')
        cls.methods = PyramidXmlRPC.methods.copy()
        cls.routes = [] + PyramidXmlRPC.routes

    @classmethod
    def tearDownClass(cls):
        super(TestPyramidXmlRPC, cls).tearDownClass()
        EnvironmentManager.set('current_blok', None)
        del RegistryManager.loaded_bloks['testPyramidXmlRPC']
        PyramidXmlRPC.methods = cls.methods
        PyramidXmlRPC.routes = cls.routes

    def setUp(self):
        super(TestPyramidXmlRPC, self).setUp()
        blokname = 'testPyramidXmlRPC'
        RegistryManager.loaded_bloks[blokname]['PyramidXmlRPC'] = {
            'registry_names': []}

    def assertInPyramidXmlRPC(self, *args):
        blokname = 'testPyramidXmlRPC'
        blok = RegistryManager.loaded_bloks[blokname]
        bases = blok['PyramidXmlRPC']['PyramidXmlRPC.MyController']['bases']
        self.assertEqual(len(bases), len(args))
        for cls_ in args:
            has = cls_ in bases
            self.assertEqual(has, True)

    def assertInRemoved(self, cls):
        core = RegistryManager.loaded_bloks['testPyramidXmlRPC']['removed']
        if cls in core:
            return True

        self.fail('Not in removed')

    def test_add_interface(self):
        register(PyramidXmlRPC, cls_=OneController, name_='MyController')
        self.assertEqual('PyramidXmlRPC',
                         PyramidXmlRPC.MyController.__declaration_type__)
        self.assertInPyramidXmlRPC(OneController)
        dir(Declarations.PyramidXmlRPC.MyController)

    def test_add_interface_with_decorator(self):

        @register(PyramidXmlRPC)
        class MyController:
            pass

        self.assertEqual('PyramidXmlRPC',
                         PyramidXmlRPC.MyController.__declaration_type__)
        self.assertInPyramidXmlRPC(MyController)

    def test_add_two_interface(self):

        register(PyramidXmlRPC, cls_=OneController, name_="MyController")

        @register(PyramidXmlRPC)
        class MyController:
            pass

        self.assertInPyramidXmlRPC(OneController, MyController)

    def test_remove_interface_with_1_cls_in_registry(self):

        register(PyramidXmlRPC, cls_=OneController, name_="MyController")
        self.assertInPyramidXmlRPC(OneController)
        unregister(PyramidXmlRPC.MyController, OneController)
        self.assertInPyramidXmlRPC(OneController)
        self.assertInRemoved(OneController)

    def test_remove_interface_with_2_cls_in_registry(self):

        register(PyramidXmlRPC, cls_=OneController, name_="MyController")

        @register(PyramidXmlRPC)
        class MyController:
            pass

        self.assertInPyramidXmlRPC(OneController, MyController)
        unregister(PyramidXmlRPC.MyController, OneController)
        self.assertInPyramidXmlRPC(MyController, OneController)
        self.assertInRemoved(OneController)
