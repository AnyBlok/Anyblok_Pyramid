# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import BlokTestCase
from pyramid.security import Allow, Deny, ALL_PERMISSIONS


class TestGetACL(BlokTestCase):

    def setUp(self):
        super(TestGetACL, self).setUp()
        self.user = self.registry.User.insert(
            login='jssuzanne', first_name='Jean-Sébastien',
            last_name='Suzanne')
        self.role = self.registry.User.Role.insert(
            name='admin', label='Administrator')
        self.role.users.append(self.user)

    def test_without_any_entry(self):
        acl = self.registry.User.Authorization.get_acl('jssuzanne', 'something')
        self.assertEqual(acl, [(Deny, 'jssuzanne', ALL_PERMISSIONS)])

    def test_with_resource(self):
        self.registry.User.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.User.Authorization.get_acl('jssuzanne', 'something')
        self.assertEqual(
            acl,
            [
                (Allow, 'jssuzanne', ['create', 'read', 'update', 'delete']),
                (Deny, 'jssuzanne', ALL_PERMISSIONS),
            ]
        )

    def test_with_wrong_resource(self):
        self.registry.User.Authorization.insert(
            resource='something2',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.User.Authorization.get_acl('jssuzanne', 'something')
        self.assertEqual(acl, [(Deny, 'jssuzanne', ALL_PERMISSIONS)])

    def test_with_model(self):
        self.registry.User.Authorization.insert(
            model='Model.System.Blok',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.User.Authorization.get_acl(
            'jssuzanne', 'Model.System.Blok')
        self.assertEqual(
            acl,
            [
                (Allow, 'jssuzanne', ['create', 'read', 'update', 'delete']),
                (Deny, 'jssuzanne', ALL_PERMISSIONS),
            ]
        )

    def test_with_resource_only_create_1(self):
        self.registry.User.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True)
        )
        acl = self.registry.User.Authorization.get_acl('jssuzanne', 'something')
        self.assertEqual(
            acl,
            [
                (Allow, 'jssuzanne', ['create']),
                (Deny, 'jssuzanne', ALL_PERMISSIONS),
            ]
        )

    def test_with_resource_only_create_2(self):
        self.registry.User.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=False),
            perm_update=dict(matched=False),
            perm_delete=dict(matched=False)
        )
        acl = self.registry.User.Authorization.get_acl('jssuzanne', 'something')
        self.assertEqual(
            acl,
            [
                (Allow, 'jssuzanne', ['create']),
                (Deny, 'jssuzanne', ['read', 'update', 'delete']),
                (Deny, 'jssuzanne', ALL_PERMISSIONS),
            ]
        )
