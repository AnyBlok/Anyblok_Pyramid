# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from pyramid.security import Allow, Deny, ALL_PERMISSIONS


@pytest.mark.usefixtures('rollback_registry')
class TestGetACL:

    @pytest.fixture(scope="function", autouse=True)
    def init_user(self, rollback_registry):
        self.registry = rollback_registry
        self.user = self.registry.Pyramid.User.insert(
            login='jssuzanne')
        self.role = self.registry.Pyramid.Role.insert(
            name='admin', label='Administrator')
        self.role.users.append(self.user)

    def test_without_any_entry(self):
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [(Deny, 'jssuzanne', ALL_PERMISSIONS)]

    def test_with_resource(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_wrong_resource(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something2',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [(Deny, 'jssuzanne', ALL_PERMISSIONS)]

    def test_with_model(self):
        self.registry.Pyramid.Authorization.insert(
            model='Model.System.Blok',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'Model.System.Blok')
        assert acl == [
            (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_resource_only_create_1(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_resource_only_create_2(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True),
            perm_read=dict(matched=False),
            perm_update=dict(matched=False),
            perm_delete=dict(matched=False)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ['delete', 'read', 'update']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_condition1(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(
                condition=dict(
                    left_condition='User.login',
                    operator='==',
                    right_value='jssuzanne',
                ),
                matched=True
            ),
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_condition2(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(
                condition=dict(
                    left_condition='User.login',
                    operator='!=',
                    right_value='jssuzanne',
                ),
                matched=True
            ),
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_condition3(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(
                condition=dict(
                    left_condition='Role.name',
                    operator='==',
                    right_value='admin',
                ),
                matched=True
            ),
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_condition4(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(
                condition=dict(
                    left_condition='Role.name',
                    operator='!=',
                    right_value='admin',
                ),
                matched=True
            ),
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_condition5(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(
                condition=dict(
                    left_condition='Role.name',
                    operator='!=',
                    right_value='admin',
                ),
                matched=True,
                unmatched=False
            ),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['delete', 'read', 'update']),
            (Deny, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_role_1(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            role=self.role,
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_role_2(self):
        self.registry.Pyramid.Role.insert(
            name='admin2', label='Other')
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            role_name='admin2',
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_role_after_login(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            role=self.role,
            perm_create=dict(matched=True),
        )
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_read=dict(matched=True),
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['read']),
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_order(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_create=dict(matched=True),
            order=2
        )
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            perm_read=dict(matched=True),
            order=1
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['read']),
            (Allow, 'jssuzanne', ['create']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_filter_1(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            filter=dict(
                left_condition='User.login',
                operator='==',
                right_value='jssuzanne'
            ),
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [
            (Allow, 'jssuzanne', ['create', 'delete', 'read', 'update']),
            (Deny, 'jssuzanne', ALL_PERMISSIONS),
        ]

    def test_with_filter_2(self):
        self.registry.Pyramid.Authorization.insert(
            resource='something',
            login='jssuzanne',
            filter=dict(
                left_condition='User.login',
                operator='!=',
                right_value='jssuzanne'
            ),
            perm_create=dict(matched=True),
            perm_read=dict(matched=True),
            perm_update=dict(matched=True),
            perm_delete=dict(matched=True)
        )
        acl = self.registry.Pyramid.Authorization.get_acl(
            'jssuzanne', 'something')
        assert acl == [(Deny, 'jssuzanne', ALL_PERMISSIONS)]
