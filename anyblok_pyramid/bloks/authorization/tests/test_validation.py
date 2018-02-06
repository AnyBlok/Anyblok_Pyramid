# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import BlokTestCase
from ..exceptions import AuthorizationValidationException


class TestAuthorizationValidation(BlokTestCase):

    def setUp(self):
        super(TestAuthorizationValidation, self).setUp()
        self.user = self.registry.User.insert(
            login='jssuzanne', first_name='Jean-Sébastien',
            last_name='Suzanne')
        self.role = self.registry.User.Role.insert(
            name='admin', label='Administrator')
        self.role.users.append(self.user)

    def get_entry_value(self):
        return dict(
            resource='Model.System.Blok',
            model='Model.System.Blok',
            primary_keys={'name': 'authorization'},
            filter={'state': 'installed'},
            role=self.role,
            login='jssuzanne',
        )

    def test_ok(self):
        vals = self.get_entry_value()
        authorization = self.registry.User.Authorization.insert(**vals)
        self.assertIs(authorization.user, self.user)

    def test_without_resource_and_model(self):
        vals = self.get_entry_value()
        del vals['resource']
        del vals['model']
        del vals['primary_keys']
        with self.assertRaises(AuthorizationValidationException):
            self.registry.User.Authorization.insert(**vals)

    def test_primary_keys_without_model(self):
        vals = self.get_entry_value()
        del vals['model']
        with self.assertRaises(AuthorizationValidationException):
            self.registry.User.Authorization.insert(**vals)

    def test_without_role_and_login(self):
        vals = self.get_entry_value()
        del vals['role']
        del vals['login']
        del vals['primary_keys']
        with self.assertRaises(AuthorizationValidationException):
            self.registry.User.Authorization.insert(**vals)
