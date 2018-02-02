# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import BlokTestCase
from ..exceptions import RecursionRoleError


class TestUserAndRole(BlokTestCase):

    def setUp(self):
        super(TestUserAndRole, self).setUp()
        self.User = self.registry.User
        self.Role = self.registry.User.Role
        self.user = self.User.insert(
            login='user.1', first_name="User", last_name="1")
        self.role = self.Role.insert(name='admin', label="Administrator")
        self.role.users.append(self.user)

    def test_role_name_in_user_roles(self):
        self.assertIn(
            self.role.name,
            self.User.get_roles(self.user.login)
        )

    def test_rec_roles(self):
        role2 = self.Role.insert(name='g2', label="G2")
        self.role.children.append(role2)
        role2.children.append(self.role)
        with self.assertRaises(RecursionRoleError):
            self.registry.flush()
