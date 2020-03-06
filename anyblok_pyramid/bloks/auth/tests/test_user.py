# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from ..exceptions import RecursionRoleError


@pytest.mark.usefixtures('rollback_registry')
class TestUserAndRole:

    def init_user(self, registry):
        self.User = registry.Pyramid.User
        self.Role = registry.Pyramid.Role
        self.user = self.User.insert(
            login='user.1')
        self.role = self.Role.insert(name='admin', label="Administrator")
        self.role.users.append(self.user)

    def test_role_name_in_user_roles(self, rollback_registry):
        self.init_user(rollback_registry)
        assert self.role.name in self.User.get_roles(self.user.login)

    def test_rec_roles(self, rollback_registry):
        self.init_user(rollback_registry)
        role2 = self.Role.insert(name='g2', label="G2")
        self.role.children.append(role2)
        role2.children.append(self.role)
        with pytest.raises(RecursionRoleError):
            rollback_registry.flush()
